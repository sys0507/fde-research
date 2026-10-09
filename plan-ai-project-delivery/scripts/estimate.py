#!/usr/bin/env python3
"""Deterministic delivery model calculator. Python standard library only."""
import argparse
import csv
import hashlib
import io
import json
import re
import sys
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

D = Decimal
CENT = D('0.01')
class ModelError(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise ModelError(message)

def dec(value, label='number', positive=False):
    require(not isinstance(value, bool), f'{label}: boolean is not a number')
    try:
        n = D(str(value))
    except (InvalidOperation, ValueError):
        raise ModelError(f'{label}: invalid decimal')
    require(n.is_finite() and n >= 0 and (not positive or n > 0), f'{label}: must be finite and {"positive" if positive else "nonnegative"}')
    return n

def day(value, label):
    require(isinstance(value, int) and not isinstance(value, bool) and value >= 1, f'{label}: positive integer required')
    return value

def money(value):
    return format(value.quantize(CENT, rounding=ROUND_HALF_UP), '.2f')

def number(value):
    return format(value, 'f')

def text_fields(obj, fields, label):
    for f in fields.split():
        require(isinstance(obj.get(f), str) and obj[f].strip(), f'{label}.{f}: nonempty text required')

def choice(obj, field, values, label):
    require(obj.get(field) in values.split(), f'{label}.{field}: expected {values}')

def index(items, label):
    require(isinstance(items, list), f'{label}: list required')
    result = {}
    for item in items:
        require(isinstance(item, dict), f'{label}: object required')
        text_fields(item, 'id', label)
        require(item['id'] not in result, f'{label}: duplicate id {item["id"]}')
        result[item['id']] = item
    return result

def refs(obj, field, universe, label):
    values = obj.get(field)
    require(isinstance(values, list) and all(isinstance(v, str) for v in values), f'{label}.{field}: string list required')
    require(len(values) == len(set(values)), f'{label}.{field}: duplicate references')
    require(all(v in universe for v in values), f'{label}.{field}: unknown reference')
    return values

def validate(m):
    require(isinstance(m, dict) and m.get('schema_version') == 1, 'schema_version must be 1')
    require(m.get('estimation_profile', 'legacy_v1') in ('legacy_v1', 'ai_collaborative_v1'), 'unknown estimation_profile')
    project = m['project']
    text_fields(project, 'name version date status currency change_reason', 'project')
    try:
        date.fromisoformat(project['date'])
    except ValueError:
        raise ModelError('project.date: ISO date required')
    dec(project['hours_per_day'], 'project.hours_per_day', True)
    reqs = index(m['requirements'], 'requirements')
    people = index(m['people'], 'people')
    packages = index(m['packages'], 'packages')
    expenses = index(m['expenses'], 'expenses')
    assumptions = index(m['assumptions'], 'assumptions')
    require(packages and people, 'at least one package and person required')
    for r in reqs.values():
        text_fields(r, 'title basis', 'requirement')
        choice(r, 'disposition', 'included excluded conditional', 'requirement')
    for p in people.values():
        text_fields(p, 'role', 'person')
        choice(p, 'payer', 'client vendor', 'person')
        dec(p['hourly_cost'], 'person.hourly_cost')
        dec(p['capacity_hours_per_day'], 'person.capacity_hours_per_day')
        a, b = day(p['available_from'], 'person.available_from'), day(p['available_to'], 'person.available_to')
        require(a <= b, 'person: inverted availability')
        require(isinstance(p.get('overrides', {}), dict), 'person.overrides: object required')
        for k, v in p.get('overrides', {}).items():
            require(re.fullmatch(r'[1-9][0-9]*', k) is not None and a <= int(k) <= b, 'override day outside availability')
            dec(v, 'override capacity')
        costing = p.get('costing', {'method': 'hourly'})
        choice(costing, 'method', 'hourly reserved_period', 'person.costing')
        if costing['method'] == 'reserved_period':
            periods = index(costing.get('periods'), 'person.costing.periods')
            require(periods, 'reserved_period requires periods')
            prior_end = 0
            for period in sorted(periods.values(), key=lambda x: x['start_day']):
                start, end = day(period['start_day'], 'cost period start'), day(period['end_day'], 'cost period end')
                require(a <= start <= end <= b and start > prior_end, 'cost periods overlap or outside availability')
                prior_end = end
                text_fields(period, 'basis', 'cost period')
                share = dec(period['allocation_share'], 'allocation_share', True)
                require(share <= 1, 'allocation_share exceeds 1')
                for field in ('salary', 'employer_contributions', 'included_overhead'):
                    amount = dec(period[field], field)
                    require(amount == D(money(amount)), 'cost period currency precision must be at most two decimal places')
            if 'outside_period_hourly_cost' in costing:
                dec(costing['outside_period_hourly_cost'], 'outside_period_hourly_cost')
                text_fields(costing, 'outside_period_basis', 'person.costing')
        else:
            require(not costing.get('periods'), 'hourly method cannot also charge reserved periods')
    covered, shared, daily = set(), set(), {}
    for p in packages.values():
        label = 'package ' + p['id']
        text_fields(p, 'title owner deliverable done_when estimate_basis', label)
        choice(p, 'kind', 'build configure reuse test deploy handover wait risk', label)
        require(p['owner'] in people, label + ': owner unknown')
        for rid in refs(p, 'requirement_ids', reqs, label):
            require(reqs[rid]['disposition'] != 'excluded', label + ': excluded requirement')
            covered.add(rid)
        a, b = day(p['start_day'], label+'.start_day'), day(p['end_day'], label+'.end_day')
        require(a <= b, label + ': inverted schedule')
        dec(p['agent_hours'], label+'.agent_hours')
        require(dec(p['external_wait_days'], label+'.external_wait_days') <= b-a+1, label + ': wait exceeds span')
        require(isinstance(p['normal_rework_included'], bool), label + ': normal_rework_included must be boolean')
        if p['kind'] == 'risk':
            text_fields(p, 'risk_reason', label)
        if 'shared_key' in p:
            text_fields(p, 'shared_key', label)
            require(p['shared_key'] not in shared, 'duplicate shared_key')
            shared.add(p['shared_key'])
        for dep in refs(p, 'depends_on', packages, label):
            require(dep != p['id'], label + ': self dependency')
        p_refs = dict(p, uses_shared=p.get('uses_shared', []))
        for sid in refs(p_refs, 'uses_shared', packages, label):
            require(sid != p['id'] and bool(packages[sid].get('shared_key')), label + ': uses_shared must reference shared package')
        require(isinstance(p['allocations'], list), label + ': allocations list required')
        for al in p['allocations']:
            pid, d = al['person_id'], day(al['day'], label+'.allocation.day')
            require(pid in people, label + ': unknown allocation person')
            require(a <= d <= b, label + ': allocation outside package')
            per = people[pid]
            require(per['available_from'] <= d <= per['available_to'], label + ': allocation outside person availability')
            costing = per.get('costing', {'method': 'hourly'})
            if costing['method'] == 'reserved_period':
                matched = [r for r in costing['periods'] if r['start_day'] <= d <= r['end_day']]
                require(matched or 'outside_period_hourly_cost' in costing, label + ': allocation outside cost periods needs explicit hourly policy')
            daily[(pid,d)] = daily.get((pid,d), D(0)) + dec(al['hours'], label+'.allocation.hours')
    require(all(r['id'] in covered for r in reqs.values() if r['disposition'] == 'included'), 'included requirement has no package')
    visiting, visited = set(), set()
    def visit(pid):
        require(pid not in visiting, 'dependency cycle')
        if pid in visited:
            return
        visiting.add(pid)
        for dep in packages[pid]['depends_on']:
            visit(dep)
        visiting.remove(pid)
        visited.add(pid)
    for pid in packages:
        visit(pid)
    for p in packages.values():
        for dep in p['depends_on']:
            require(p['start_day'] > packages[dep]['end_day'], f'{p["id"]}: dependency must finish before start')
    for (pid,d), hours in daily.items():
        p = people[pid]
        require(hours <= dec(p.get('overrides', {}).get(str(d), p['capacity_hours_per_day'])), f'capacity exceeded: {pid} day {d} ({hours} hours)')
    for e in expenses.values():
        text_fields(e, 'title basis', 'expense')
        choice(e, 'payer', 'client vendor', 'expense')
        choice(e, 'period', 'one_time month year', 'expense')
        choice(e, 'category', 'api compute tool other equipment', 'expense')
        choice(e, 'purpose', 'development production other', 'expense')
        refs(e, 'task_ids', packages, 'expense')
        require(e['amount'] is not None or e['category'] == 'equipment' or (e.get('quote_status') == 'unquoted' and e['payer'] == 'client'), 'only equipment or explicitly unquoted client expense can have unknown amount')
        if 'quote_status' in e:
            choice(e, 'quote_status', 'estimated quoted unquoted', 'expense')
            require((e['amount'] is None) == (e['quote_status'] == 'unquoted'), 'unquoted status requires unknown amount')
        if e['amount'] is not None:
            require(dec(e['amount'], 'expense.amount') == D(money(dec(e['amount']))), 'expense.amount: currency precision must be at most two decimal places')
        if 'api' in e:
            require(e['category'] == 'api', 'api detail requires api category')
            api = e['api']
            text_fields(api, 'model price_date source usage_basis', 'api')
            require(isinstance(api['lines'], list) and api['lines'], 'api.lines required')
            estimate = D(0)
            for line in api['lines']:
                text_fields(line, 'kind', 'api.line')
                estimate += dec(line['quantity_million_tokens']) * dec(line['price_per_million'])
            if 'usage_status' in api:
                choice(api, 'usage_status', 'estimated measured', 'api')
            budget = dec(api['budget'], 'api.budget')
            require(budget >= estimate and budget == dec(e['amount']), 'api budget must equal amount and cover usage estimate')
    pricing = m['pricing']
    choice(pricing, 'method', 'gross_margin markup fixed', 'pricing')
    choice(pricing, 'payment_basis', 'ex_tax inc_tax', 'pricing')
    text_fields(pricing, 'tax_note validity payment_terms_status', 'pricing')
    if pricing['method'] == 'fixed':
        dec(pricing['fixed_price'], 'fixed_price')
    else:
        rate = dec(pricing['rate'], 'rate')
        require(pricing['method'] != 'gross_margin' or rate < 1, 'gross margin must be below 1')
    if pricing['tax_rate'] is None:
        require(pricing['payment_basis'] == 'ex_tax', 'unknown tax only supports ex_tax payments')
    else:
        dec(pricing['tax_rate'], 'tax_rate')
    payments = index(pricing['payments'], 'payments')
    for p in payments.values():
        text_fields(p, 'milestone', 'payment')
    require(sum((dec(p['ratio'], 'payment.ratio') for p in payments.values()), D(0)) == 1, 'payment ratios must sum to 1')
    for a in assumptions.values():
        choice(a, 'visibility', 'client internal', 'assumption')
        choice(a, 'status', 'fact preset confirmed revised', 'assumption')
        text_fields(a, 'statement reason basis affects verify change_action', 'assumption')
    if m.get('estimation_profile') == 'ai_collaborative_v1':
        validate_collaborative(m)
    return m

def validate_collaborative(m):
    """Trace evidence and exact person-hour/token conservation, not semantic truth."""
    people = {p['id']: p for p in m['people']}
    all_agent_work = {}
    for p in m['packages']:
        label = 'package ' + p['id']
        efforts = index(p.get('human_effort'), label + '.human_effort')
        derived, allocated = {}, {}
        for h in efforts.values():
            text_fields(h, 'person_id activity unit basis', label + '.human_effort')
            require(h['person_id'] in people, label + ': effort person unknown')
            choice(h, 'category', 'prepare decide review integrate verify coordinate manual_implementation', label + '.human_effort')
            hours = dec(h['quantity'], 'effort.quantity', True) * dec(h['unit_hours'], 'effort.unit_hours', True)
            derived[h['person_id']] = derived.get(h['person_id'], D(0)) + hours
        for a in p['allocations']:
            allocated[a['person_id']] = allocated.get(a['person_id'], D(0)) + dec(a['hours'])
        require({k:v for k,v in allocated.items() if v} == derived, label + ': human_effort must equal allocations for each person')
        agents = index(p.get('agent_work'), label + '.agent_work')
        require(bool(agents) == (dec(p['agent_hours']) > 0), label + ': agent_work and agent_hours must agree')
        if not agents:
            text_fields(p, 'no_agent_work_reason', label)
        for a in agents.values():
            text_fields(a, 'activity output verification reviewer runtime_basis', label + '.agent_work')
            require(a['reviewer'] in people, label + ': Agent reviewer unknown')
            review_ids = refs(a, 'review_effort_ids', efforts, label + '.agent_work')
            require(review_ids and all(efforts[r]['person_id'] == a['reviewer'] and efforts[r]['category'] in ('review', 'verify', 'integrate') for r in review_ids), label + ': Agent review requires counted reviewer effort')
            all_agent_work[p['id'] + ':' + a['id']] = p['id']
        dependencies = p.get('dependency_basis')
        require(isinstance(dependencies, list), label + '.dependency_basis: list required')
        seen = set()
        for d in dependencies:
            text_fields(d, 'predecessor_id required_output why_blocks_start', label + '.dependency_basis')
            choice(d, 'kind', 'technical external acceptance', label + '.dependency_basis')
            require(d['predecessor_id'] not in seen, label + ': duplicate dependency evidence')
            seen.add(d['predecessor_id'])
        require(seen == set(p['depends_on']), label + ': dependency_basis must cover depends_on exactly')
    for expense in m['expenses']:
        if expense['category'] != 'api' or expense['purpose'] != 'development':
            continue
        require('api' in expense, 'development API requires task-based api detail')
        api = expense['api']
        groups = index(api.get('request_groups'), 'api.request_groups')
        require(groups, 'api.request_groups required')
        expected, priced = {}, {}
        for g in groups.values():
            text_fields(g, 'model phase iteration_basis evidence', 'api.request_group')
            linked = refs(g, 'agent_work_refs', all_agent_work, 'api.request_group')
            require(linked and all(all_agent_work[r] in expense['task_ids'] for r in linked), 'API Agent task must be in expense.task_ids')
            requests = day(g['runs'], 'API runs') * day(g['requests_per_run'], 'API requests_per_run')
            components = index(g.get('context_components'), 'API context_components')
            require(components, 'API context components required')
            for c in components.values():
                text_fields(c, 'description basis', 'API context component')
            input_tokens = sum((dec(c['tokens'], 'context.tokens') for c in components.values()), D(0))
            require(input_tokens > 0, 'API input context must be positive')
            for token_type, tokens in [('input', input_tokens), ('output', dec(g['output_tokens_per_request'], 'API output tokens', True))]:
                key = (g['model'], token_type)
                expected[key] = expected.get(key, D(0)) + requests * tokens / D(1000000)
        for line in api['lines']:
            text_fields(line, 'model', 'API line')
            choice(line, 'token_type', 'input output', 'API line')
            key = (line['model'], line['token_type'])
            priced[key] = priced.get(key, D(0)) + dec(line['quantity_million_tokens'])
        require(expected == priced, 'API token quantities must equal request_groups by model and input/output')
        usage = sum((dec(l['quantity_million_tokens']) * dec(l['price_per_million']) for l in api['lines']), D(0))
        if dec(api['budget']) > usage:
            text_fields(api, 'buffer_basis', 'API')

def table(headers, rows):
    def cell(x):
        return str(x).replace('|', '\\|').replace('\n', ' ')
    return '\n'.join(['| ' + ' | '.join(map(cell, headers)) + ' |', '| ' + ' | '.join(['---']*len(headers)) + ' |'] + ['| ' + ' | '.join(map(cell, row)) + ' |' for row in rows])

def split_money(total, weights):
    if not weights:
        return []
    denominator = sum(weights, D(0))
    if denominator == 0:
        weights = [D(1)] * len(weights)
        denominator = D(len(weights))
    amounts, remaining = [], total
    for weight in weights[:-1]:
        amount = min(D(money(total*weight/denominator)), remaining)
        amounts.append(amount)
        remaining -= amount
    return amounts + [remaining]

def calculate(m):
    validate(m)
    people = {p['id']:p for p in m['people']}
    totals = {'vendor':D(0), 'client':D(0)}
    hours = {'vendor':D(0), 'client':D(0)}
    workload, packages, quote_weights, cost_rows = [], [], {}, []
    # Period reservation is a cash/economic commitment, independent of active hours.
    allocation_costs, labor_reservations, unallocated = {}, [], []
    for person in people.values():
        costing = person.get('costing', {'method': 'hourly'})
        if costing['method'] != 'reserved_period':
            continue
        for period in costing['periods']:
            full = sum((dec(period[k]) for k in ('salary', 'employer_contributions', 'included_overhead')), D(0))
            committed = D(money(full * dec(period['allocation_share'])))
            selected = [(p['id'], i, dec(a['hours'])) for p in m['packages'] for i,a in enumerate(p['allocations']) if a['person_id'] == person['id'] and period['start_day'] <= a['day'] <= period['end_day'] and dec(a['hours']) > 0]
            active_hours = sum((x[2] for x in selected), D(0))
            row = dict(person_id=person['id'], period_id=period['id'], payer=person['payer'], start_day=period['start_day'], end_day=period['end_day'], salary=money(dec(period['salary'])), employer_contributions=money(dec(period['employer_contributions'])), included_overhead=money(dec(period['included_overhead'])), allocation_share=number(dec(period['allocation_share'])), active_hours=number(active_hours), committed_cost=money(committed), basis=period['basis'])
            labor_reservations.append(row)
            if selected:
                for (pid,i,_), cost in zip(selected, split_money(committed,[x[2] for x in selected])):
                    allocation_costs[(pid,i)] = cost
            else:
                unallocated.append(row)
    for row in unallocated:
        cost = dec(row['committed_cost'])
        totals[row['payer']] += cost
        if row['payer'] == 'vendor':
            key = 'reservation:'+row['person_id']+':'+row['period_id']
            quote_weights[key] = dict(id=key, title='Project delivery resource reservation', weight=cost)
    for p in m['packages']:
        ph, pc = D(0), D(0)
        for allocation_index, a in enumerate(p['allocations']):
            person = people[a['person_id']]
            h = dec(a['hours'])
            costing = person.get('costing', {'method': 'hourly'})
            mode = costing['method']
            if mode == 'reserved_period':
                in_period = any(r['start_day'] <= a['day'] <= r['end_day'] for r in costing['periods'])
                c = allocation_costs.get((p['id'], allocation_index), D(0)) if in_period else D(money(h*dec(costing['outside_period_hourly_cost'])))
                mode = 'reserved_period_allocation' if in_period else 'outside_period_hourly'
            else:
                c = D(money(h*dec(person['hourly_cost'])))
            totals[person['payer']] += c
            hours[person['payer']] += h
            ph += h
            if person['payer'] == 'vendor':
                pc += c
            workload.append(dict(package_id=p['id'], person_id=a['person_id'], payer=person['payer'], day=a['day'], hours=number(h), internal_cost=money(c), cost_method=mode))
        packages.append(dict(id=p['id'], title=p['title'], start_day=p['start_day'], end_day=p['end_day'], owner=p['owner'], person_hours=number(ph), vendor_labor_cost=money(pc), agent_hours=number(dec(p['agent_hours'])), external_wait_days=number(dec(p['external_wait_days'])), deliverable=p['deliverable'], depends_on=p['depends_on']))
        if pc:
            quote_weights[p['id']] = {'id':p['id'], 'title':p['title'], 'weight':pc}
    service = totals['vendor']
    client_one, client_api = D(0), D(0)
    recurring, equipment, api_results, unquoted_expenses, api_details = {}, [], [], [], []
    for e in m['expenses']:
        amount = dec(e['amount']) if e['amount'] is not None else None
        cost_rows.append(dict(id=e['id'], title=e['title'], payer=e['payer'], period=e['period'], category=e['category'], purpose=e['purpose'], amount=money(amount) if amount is not None else None, included_in_service=e['payer']=='vendor' and e['period']=='one_time' and e['category']!='equipment'))
        if e['category'] == 'equipment':
            equipment.append(cost_rows[-1])
        elif amount is None:
            unquoted_expenses.append(cost_rows[-1])
        elif e['period'] != 'one_time':
            key = e['payer'] + ':' + e['period']
            recurring[key] = recurring.get(key, D(0)) + amount
        elif e['payer'] == 'vendor':
            service += amount
            if e['task_ids']:
                for pid in e['task_ids']:
                    if pid not in quote_weights:
                        p = next(p for p in m['packages'] if p['id'] == pid)
                        quote_weights[pid] = dict(id=pid, title=p['title'], weight=D(0))
                    quote_weights[pid]['weight'] += amount/D(len(e['task_ids']))
            else:
                quote_weights['expense:'+e['id']] = dict(id='expense:'+e['id'], title=e['title'], weight=amount)
        else:
            client_one += amount
            if e['category'] == 'api' and e['purpose'] == 'development':
                client_api += amount
        if 'api' in e:
            api = e['api']
            usage = sum((dec(l['quantity_million_tokens'])*dec(l['price_per_million']) for l in api['lines']), D(0))
            api_details.append(dict(expense_id=e['id'], payer=e['payer'], purpose=e['purpose'], model=api['model'], usage_status=api.get('usage_status','estimated'), price_date=api['price_date'], source=api['source'], usage_basis=api['usage_basis'], lines=api['lines']))
            api_results.append(dict(expense_id=e['id'], usage_estimate=money(usage), budget=money(dec(api['budget'])), buffer=money(dec(api['budget'])-usage)))
    pricing = m['pricing']
    method = pricing['method']
    raw_price = dec(pricing['fixed_price']) if method=='fixed' else service/(1-dec(pricing['rate'])) if method=='gross_margin' else service*(1+dec(pricing['rate']))
    price = D(money(raw_price))
    tax = D(money(price*dec(pricing['tax_rate']))) if pricing['tax_rate'] is not None else None
    inc = price+tax if tax is not None else None
    payment_total = inc if pricing['payment_basis']=='inc_tax' else price
    payment_amounts = split_money(payment_total, [dec(p['ratio']) for p in pricing['payments']])
    payments = [dict(id=p['id'], milestone=p['milestone'], ratio=number(dec(p['ratio'])), amount=money(a)) for p,a in zip(pricing['payments'],payment_amounts)]
    if not quote_weights:
        quote_weights['service'] = dict(id='service', title='Project services', weight=D(1))
    quote_amounts = split_money(price, [q['weight'] for q in quote_weights.values()])
    quotes = [dict(id=q['id'], title=q['title'], service_price_ex_tax=money(a)) for q,a in zip(quote_weights.values(),quote_amounts)]
    duration = max(p['end_day'] for p in packages)-min(p['start_day'] for p in packages)+1
    public = dict(service_price_ex_tax=money(price), tax_amount=money(tax) if tax is not None else 'Pending confirmation', service_price_inc_tax=money(inc) if inc is not None else 'Pending confirmation', payment_total=money(payment_total), vendor_person_hours=number(hours['vendor']), duration_days=str(duration), client_one_time_known=money(client_one), client_development_api_budget=money(client_api), client_incremental_known=money(payment_total+client_one))
    public['public_schedule_table'] = table(['Work package','Owner','Start day','End day','Deliverable'], [[p['title'],people[p['owner']]['role']+' ('+p['owner']+')',p['start_day'],p['end_day'],p['deliverable']] for p in packages])
    public['public_payment_table'] = table(['Milestone','Share','Amount ('+{'ex_tax':'excluding tax','inc_tax':'including tax'}[pricing['payment_basis']]+')'], [[p['milestone'],number(dec(p['ratio'])*100)+'%',p['amount']] for p in payments])
    public['public_quote_table'] = table(['Service item','Price excluding tax'], [[q['title'],q['service_price_ex_tax']] for q in quotes])
    public['public_expense_table'] = table(['Expense','Payer','Period','Amount','Notes'], [[e['title'],{'client':'Client','vendor':'Vendor'}[e['payer']],{'one_time':'One-time','month':'Monthly','year':'Annual'}[e['period']],money(dec(e['amount'])) if e['amount'] is not None else 'To be determined', 'Equipment quoted separately' if e['category']=='equipment' else 'Recurring expense listed separately' if e['period']!='one_time' else 'Client expense' ] for e in m['expenses'] if e['payer']=='client'])
    public['public_api_basis_table'] = table(['Item','Model and price date','Usage status and basis','Estimated cost','Budget'], [[e['title'],e['api']['model']+' / '+e['api']['price_date'],('Measured trace' if e['api'].get('usage_status')=='measured' else 'Estimation assumption')+': '+e['api']['usage_basis'],next(a['usage_estimate'] for a in api_results if a['expense_id']==e['id']),money(dec(e['amount']))] for e in m['expenses'] if e['payer']=='client' and 'api' in e])
    result = dict(schema_version=1, project=m['project'], service_cost=money(service), labor_cost={k:money(v) for k,v in totals.items()}, person_hours={k:number(v) for k,v in hours.items()}, vendor_person_days=number(hours['vendor']/dec(m['project']['hours_per_day'])), duration_days=duration, service_price_ex_tax=money(price), tax_amount=money(tax) if tax is not None else None, service_price_inc_tax=money(inc) if inc is not None else None, payment_total=money(payment_total), payment_basis=pricing['payment_basis'], gross_profit=money(price-service), actual_gross_margin=number((price-service)/price) if price else None, client_one_time_known=money(client_one), client_development_api_budget=money(client_api), client_incremental_known=money(payment_total+client_one), recurring={k:money(v) for k,v in sorted(recurring.items())}, equipment=equipment, unquoted_expenses=unquoted_expenses, api_estimates=api_results, api_usage_details=api_details, labor_reservations=labor_reservations, workload=workload, costs=cost_rows, packages=packages, payments=payments, quote_items=quotes, public_facts=public)

    if m.get('estimation_profile') == 'ai_collaborative_v1':
        result['estimation_profile'] = m['estimation_profile']
        result['effort_details'] = [dict(package_id=p['id'], **h, hours=number(dec(h['quantity'])*dec(h['unit_hours']))) for p in m['packages'] for h in p['human_effort']]
        result['agent_work_details'] = [dict(package_id=p['id'], **a) for p in m['packages'] for a in p['agent_work']]
        result['dependency_evidence'] = [dict(package_id=p['id'], **d) for p in m['packages'] for d in p['dependency_basis']]
        result['api_request_groups'] = [dict(expense_id=e['id'], **g) for e in m['expenses'] if 'api' in e for g in e['api'].get('request_groups', [])]
    return result

def read_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f, parse_float=str)

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)+'\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def csv_write(path, rows, headers):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)

def diff(old, new):
    return {key:{'before':old.get(key), 'after':new.get(key)} for key in sorted(set(old)|set(new)) if old.get(key)!=new.get(key)}

def check(directory):
    directory = Path(directory)
    manifest = read_json(directory/'manifest.json')
    for filename, digest in manifest['files'].items():
        path = (directory/filename).resolve()
        require(path.is_relative_to(directory.resolve()) and path != directory.resolve(), 'manifest path outside version directory')
        require(path.is_file() and sha(path)==digest, 'hash mismatch: '+filename)
    results = read_json(directory/'results.json')
    recalculated = calculate(read_json(directory/'model.json'))
    # Old v1 runs omit only these newly introduced explanatory outputs.
    # Preserve strict equality for all original numerical and public fields.
    for key in ('labor_reservations', 'api_usage_details', 'unquoted_expenses'):
        if key not in results:
            recalculated.pop(key)
    if 'public_api_basis_table' not in results['public_facts']:
        recalculated['public_facts'].pop('public_api_basis_table')
    if all('cost_method' not in row for row in results['workload']):
        for row in recalculated['workload']:
            row.pop('cost_method')
    require(recalculated == results, 'results differ from recalculation')
    for record in manifest.get('renders', []):
        require(record['results_sha256']==sha(directory/'results.json'), 'render results signature mismatch')
        require(all(results['public_facts'].get(k)==v for k,v in record['facts'].items()), 'render fact mismatch')
        require(record['file'] in manifest['files'], 'render missing file signature')
        content = record['template']
        require(hashlib.sha256(content.encode()).hexdigest()==record['template_sha256'], 'template signature mismatch')
        for token in tokens(content):
            require(token in record['facts'], 'render token missing fact')
        expected = substitute(content, record['facts'])
        require((directory/record['file']).read_text(encoding='utf-8') == expected, 'render content mismatch')
    return True

def run(model_path, output, previous=None):
    m = read_json(model_path)
    result = calculate(m)
    out = Path(output)
    require(not out.exists(), 'output directory already exists; choose a new version')
    changes = {'previous':None, 'input_changes':{}, 'result_changes':{}}
    if previous:
        check(previous)
        previous = Path(previous)
        old = read_json(previous/'model.json')
        require(old['project']['version'] != m['project']['version'], 'new version must differ from previous')
        changes = dict(previous=str(previous.resolve()), previous_manifest_sha256=sha(previous/'manifest.json'), input_changes=diff(old,m), result_changes=diff(read_json(previous/'results.json'),result))
    out.mkdir(parents=True)
    write_json(out/'model.json', m)
    write_json(out/'results.json', result)
    write_json(out/'changes.json', changes)
    if 'effort_details' in result:
        csv_write(out/'activity-workload.csv', result['effort_details'], ['package_id','id','person_id','category','activity','quantity','unit','unit_hours','hours','basis'])
        write_json(out/'collaboration-evidence.json', {k:result[k] for k in ('agent_work_details','dependency_evidence','api_request_groups')})
    csv_write(out/'workload.csv',result['workload'],['package_id','person_id','payer','day','hours','internal_cost','cost_method'])
    csv_write(out/'labor-reservations.csv',result['labor_reservations'],['person_id','period_id','payer','start_day','end_day','salary','employer_contributions','included_overhead','allocation_share','active_hours','committed_cost','basis'])
    csv_write(out/'costs.csv',result['costs'],['id','title','payer','period','category','purpose','amount','included_in_service'])
    csv_write(out/'schedule.csv',result['packages'],['id','title','owner','start_day','end_day','person_hours','agent_hours','external_wait_days','deliverable','depends_on'])
    csv_write(out/'payments.csv',result['payments'],['id','milestone','ratio','amount'])
    facts = '# Numeric facts (internal workbook)\n\n## Public facts\n\n'+ '\n\n'.join(f'### {k}\n\n{v}' for k,v in result['public_facts'].items())
    facts += '\n\n## Internal facts\n\nService cost: '+result['service_cost']+'\n\nBalance on the model cost basis (not after-tax profit): '+result['gross_profit']+'\n\nKnown client incremental funding excludes recurring production costs, equipment, client labor, and unknown amounts.\n'
    (out/'numeric-facts.md').write_text(facts, encoding='utf-8')
    manifest = dict(schema_version=1, files={p.name:sha(p) for p in sorted(out.iterdir())}, renders=[])
    write_json(out/'manifest.json',manifest)
    check(out)
    return result

TOKEN = re.compile(r'\{\{\s*([A-Za-z_][A-Za-z_0-9]*)\s*\}\}')
def tokens(template):
    names = TOKEN.findall(template)
    stripped = TOKEN.sub('', template)
    require('{{' not in stripped and '}}' not in stripped, 'invalid template token')
    return names

def substitute(template, facts):
    for name in tokens(template):
        require(name in facts, 'unknown or internal token: '+name)
    return TOKEN.sub(lambda match:str(facts[match.group(1)]), template)

def render(results_path, template_path, output):
    rp, op = Path(results_path).resolve(), Path(output).resolve()
    require(rp.name == 'results.json', 'render requires version results.json')
    require(op.is_relative_to(rp.parent), 'render output must stay inside result directory')
    require(op.suffix == '.md', 'render output must be Markdown')
    require(not op.exists(), 'render output already exists')
    check(rp.parent)
    result = read_json(rp)
    template = Path(template_path).read_text(encoding='utf-8')
    names = tokens(template)
    require(names, 'template must contain at least one controlled numeric token')
    content = substitute(template, result['public_facts'])
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(content, encoding='utf-8')
    relative_name = op.relative_to(rp.parent).as_posix()
    manifest = read_json(rp.parent/'manifest.json')
    manifest['files'][relative_name] = sha(op)
    manifest['renders'].append(dict(file=relative_name, results_sha256=sha(rp), template=template, template_sha256=hashlib.sha256(template.encode()).hexdigest(), facts={k:result['public_facts'][k] for k in names}))
    write_json(rp.parent/'manifest.json',manifest)
    check(rp.parent)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    for name in ('validate','run'):
        p = sub.add_parser(name)
        p.add_argument('--model',required=True)
        p.add_argument('--allow-legacy', action='store_true', help='Explicit compatibility for historical models without AI activity evidence')
        if name=='run':
            p.add_argument('--output',required=True)
            p.add_argument('--previous')
    p = sub.add_parser('render')
    for name in ('results','template','output'):
        p.add_argument('--'+name,required=True)
    sub.add_parser('check').add_argument('--output',required=True)
    args = parser.parse_args()
    try:
        if args.command in ('validate','run'):
            require(args.allow_legacy or read_json(args.model).get('estimation_profile') == 'ai_collaborative_v1', 'new runs require ai_collaborative_v1; use --allow-legacy only for historical compatibility')
        if args.command=='validate':
            validate(read_json(args.model))
        elif args.command=='run':
            run(args.model,args.output,args.previous)
        elif args.command=='render':
            render(args.results,args.template,args.output)
        else:
            check(args.output)
        print('PASS '+args.command)
    except (ModelError, KeyError, TypeError, ValueError, OSError, ArithmeticError) as e:
        print('ERROR: '+str(e),file=sys.stderr)
        return 2
    return 0
if __name__=='__main__':
    sys.exit(main())
