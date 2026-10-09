#!/usr/bin/env python3
import copy
import hashlib
import json
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path
import estimate as e
ROOT = Path(__file__).resolve().parents[1]
class EstimateTests(unittest.TestCase):
    def setUp(self):
        self.m = e.read_json(ROOT/'assets/example-model.json')
        self.m['estimation_profile']='legacy_v1'
    def bad(self, edit, pattern=None):
        edit(self.m)
        with self.assertRaisesRegex((e.ModelError,KeyError), pattern or '.'):
            e.validate(self.m)
    def test_sample_and_separation(self):
        r=e.calculate(self.m)
        self.assertEqual(r['service_cost'],'27600.00')
        self.assertEqual(r['service_price_ex_tax'],'36800.00')
        self.assertEqual(r['client_incremental_known'],'36820.00')
        self.assertEqual(r['person_hours']['vendor'],'144')
        self.assertEqual(r['duration_days'],15)
        self.assertEqual(r['api_estimates'][0],dict(expense_id='E2',usage_estimate='12.10',budget='20.00',buffer='7.90'))
        self.assertIsNone(r['equipment'][0]['amount'])
        self.assertEqual(r['recurring'],{'client:month':'1000.00'})
        self.assertEqual(sum(D(x['service_price_ex_tax']) for x in r['quote_items']),D('36800'))
    def test_pricing_methods(self):
        self.m['pricing'].update(method='markup',rate='.25')
        self.assertEqual(e.calculate(self.m)['service_price_ex_tax'],'34500.00')
        self.m['pricing'].update(method='fixed',fixed_price='123.45')
        self.assertEqual(e.calculate(self.m)['service_price_ex_tax'],'123.45')
    def test_tax_and_payment_rounding(self):
        self.m['pricing'].update(method='fixed',fixed_price='0.05',tax_rate='.06',payment_basis='inc_tax')
        r=e.calculate(self.m)
        self.assertEqual(r['tax_amount'],'0.00')
        self.assertEqual([p['amount'] for p in r['payments']],['0.02','0.02','0.01'])
        self.assertEqual(sum(D(p['amount']) for p in r['payments']),D(r['payment_total']))
        self.m['pricing']['fixed_price']='36800'
        r=e.calculate(self.m)
        self.assertEqual(r['tax_amount'],'2208.00')
        self.assertEqual(r['payment_total'],'39008.00')
    def test_fractional_cost_reconciles(self):
        self.m['people'][0]['hourly_cost']='.3333'
        r=e.calculate(self.m)
        total=sum(D(row['internal_cost']) for row in r['workload'] if row['payer']=='vendor')
        self.assertEqual(total,D(r['labor_cost']['vendor']))
        self.assertEqual(D(r['service_cost']),total+D('800'))
    def test_tiny_payment_never_negative(self):
        self.m['pricing'].update(method='fixed',fixed_price='.01')
        for p,r in zip(self.m['pricing']['payments'],['.5','.5','0']): p['ratio']=r
        amounts=[D(p['amount']) for p in e.calculate(self.m)['payments']]
        self.assertEqual(sum(amounts),D('.01'))
        self.assertTrue(all(a>=0 for a in amounts))
    def test_public_expenses_hide_vendor_costs(self):
        self.m['expenses'][2].update(payer='vendor',amount='9876.54')
        r=e.calculate(self.m)
        self.assertNotIn('9876.54',r['public_facts']['public_expense_table'])
    def test_public_tables_use_customer_language(self):
        r=e.calculate(self.m)
        facts=r['public_facts']
        self.assertIn('Amount (excluding tax)',facts['public_payment_table'])
        self.assertIn('Client',facts['public_expense_table'])
        self.assertIn('One-time',facts['public_expense_table'])
        self.assertIn('Monthly',facts['public_expense_table'])
        self.assertIn('FDE engineer (fde)',facts['public_schedule_table'])
        for enum in ['client','vendor','one_time','month','year','ex_tax','inc_tax']:
            self.assertNotIn(enum,facts['public_expense_table']+facts['public_payment_table'])
        self.m['pricing'].update(tax_rate='.06',payment_basis='inc_tax')
        self.m['expenses'][2]['period']='year'
        facts=e.calculate(self.m)['public_facts']
        self.assertIn('Amount (including tax)',facts['public_payment_table'])
        self.assertIn('Annual',facts['public_expense_table'])
    def test_production_api_not_development(self):
        self.m['expenses'][1]['purpose']='production'
        r=e.calculate(self.m)
        self.assertEqual(r['client_development_api_budget'],'0.00')
        self.assertEqual(r['client_one_time_known'],'20.00')
    def test_client_labor_not_service(self):
        self.m['people'][1]['payer']='client'
        r=e.calculate(self.m)
        self.assertEqual(r['service_cost'],'24600.00')
        self.assertEqual(r['labor_cost']['client'],'3000.00')
    def test_vendor_recurring_not_service(self):
        self.m['expenses'][2]['payer']='vendor'
        r=e.calculate(self.m)
        self.assertEqual(r['service_cost'],'27600.00')
        self.assertEqual(r['recurring'],{'vendor:month':'1000.00'})
    def test_unknown_tax(self): self.bad(lambda m:m['pricing'].update(payment_basis='inc_tax'),'unknown tax')
    def test_payment_bad_sum(self): self.bad(lambda m:m['pricing']['payments'][0].update(ratio='.4'),'sum to 1')
    def test_capacity(self): self.bad(lambda m:m['people'][0].update(capacity_hours_per_day='7'),'capacity')
    def test_capacity_override(self): self.bad(lambda m:m['people'][0].update(overrides={'1':'0'}),'capacity')
    def test_availability(self): self.bad(lambda m:m['people'][0].update(available_from=2),'availability')
    def test_cycle(self): self.bad(lambda m:m['packages'][0].update(depends_on=['P2']),'cycle')
    def test_inverted_dependency(self): self.bad(lambda m:m['packages'][3].update(depends_on=['P3']),'finish before')
    def test_duplicate_id(self): self.bad(lambda m:m['packages'][1].update(id='P1'),'duplicate id')
    def test_duplicate_shared(self): self.bad(lambda m:m['packages'][1].update(shared_key='shared-retrieval'),'shared_key')
    def test_bad_shared_reference(self): self.bad(lambda m:m['packages'][2].update(uses_shared=['P4']),'shared package')
    def test_negative_day(self): self.bad(lambda m:m['packages'][0].update(start_day=-1),'positive integer')
    def test_nonfinite(self): self.bad(lambda m:m['people'][0].update(hourly_cost='NaN'),'finite')
    def test_nonfinite_infinity(self): self.bad(lambda m:m['expenses'][0].update(amount='Infinity'),'finite')
    def test_negative_amount(self): self.bad(lambda m:m['expenses'][0].update(amount='-1'),'nonnegative')
    def test_amount_precision(self): self.bad(lambda m:m['expenses'][0].update(amount='.001'),'precision')
    def test_unknown_payer(self): self.bad(lambda m:m['expenses'][0].update(payer='someone'),'payer')
    def test_unknown_period(self): self.bad(lambda m:m['expenses'][0].update(period='week'),'period')
    def test_purpose_required(self): self.bad(lambda m:m['expenses'][0].pop('purpose'),'purpose')
    def test_null_non_equipment(self): self.bad(lambda m:m['expenses'][0].update(amount=None),'equipment')
    def test_owner(self): self.bad(lambda m:m['packages'][0].update(owner='nobody'),'owner')
    def test_risk_reason(self): self.bad(lambda m:m['packages'][4].update(risk_reason=''),'risk_reason')
    def test_wait(self): self.bad(lambda m:m['packages'][0].update(external_wait_days=2),'wait exceeds')
    def test_uncovered_requirement(self): self.bad(lambda m:m['requirements'].append(dict(id='R4',title='Other',disposition='included',basis='test')),'no package')
    def test_excluded_requirement(self): self.bad(lambda m:m['requirements'][0].update(disposition='excluded'),'excluded')
    def test_version_render_and_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            t=Path(td); model=t/'input.json'; e.write_json(model,self.m)
            v1=t/'v1'; e.run(model,v1)
            before={str(p.relative_to(v1)):e.sha(p) for p in v1.rglob('*') if p.is_file()}
            with self.assertRaises(e.ModelError): e.run(model,v1)
            self.m['project'].update(version='v2',change_reason='Update resource expenses')
            self.m['expenses'][0]['amount']='1000'
            e.write_json(model,self.m); v2=t/'v2'; e.run(model,v2,v1)
            self.assertEqual(before,{str(p.relative_to(v1)):e.sha(p) for p in v1.rglob('*') if p.is_file()})
            self.assertIn('expenses',e.read_json(v2/'changes.json')['input_changes'])
            self.assertIn('service_cost',e.read_json(v2/'changes.json')['result_changes'])
            template=t/'template.md'; template.write_text('Quotation {{service_price_ex_tax}}\n{{public_quote_table}}\n{{public_payment_table}}\n{{public_schedule_table}}\n{{public_expense_table}}', encoding='utf-8')
            client=v2/'client/report.md'; e.render(v2/'results.json',template,client)
            self.assertTrue(e.check(v2))
            self.assertIn('37066.67',client.read_text(encoding='utf-8'))
            template.write_text('{{service_cost}}', encoding='utf-8')
            with self.assertRaisesRegex(e.ModelError,'internal token'): e.render(v2/'results.json',template,v2/'client/leak.md')
            template.write_text('{{nonexistent}}', encoding='utf-8')
            with self.assertRaises(e.ModelError): e.render(v2/'results.json',template,v2/'client/unknown.md')
            template.write_text('{{service_price_ex_tax}}', encoding='utf-8')
            with self.assertRaises(e.ModelError): e.render(v2/'results.json',template,t/'escape.md')
            outside=t/'outside'; outside.mkdir(); (v2/'symlink').symlink_to(outside,target_is_directory=True)
            with self.assertRaises(e.ModelError): e.render(v2/'results.json',template,v2/'symlink/leak.md')
            client.write_text(client.read_text(encoding='utf-8')+' tampered', encoding='utf-8')
            with self.assertRaisesRegex(e.ModelError,'hash mismatch'): e.check(v2)
class ReservationTests(unittest.TestCase):
    def setUp(self):
        self.m=e.read_json(ROOT/'assets/reserved-period-example.json')
        self.m['estimation_profile']='legacy_v1'
    def test_reserved_baseline_and_separation(self):
        r=e.calculate(self.m)
        self.assertEqual(r['service_cost'],'33620.00')
        self.assertEqual(r['labor_cost']['vendor'],'31520.00')
        self.assertEqual(r['person_hours']['vendor'],'156')
        self.assertEqual(r['service_price_ex_tax'],'42500.00')
        self.assertEqual(r['gross_profit'],'8880.00')
        self.assertEqual(r['client_incremental_known'],'42640.00')
        self.assertEqual(r['labor_reservations'][0]['committed_cost'],'28800.00')
        self.assertEqual(r['labor_reservations'][0]['active_hours'],'140')
        self.assertEqual(r['unquoted_expenses'][0]['amount'],None)
        self.assertEqual(r['recurring'],{})
    def test_active_hours_do_not_reduce_salary(self):
        self.m['packages'][0]['allocations'][0]['hours']='1'
        r=e.calculate(self.m)
        self.assertEqual(r['service_cost'],'33620.00')
        self.assertEqual(r['person_hours']['vendor'],'150')
    def test_legacy_rate_cannot_duplicate_reserved_salary(self):
        self.m['people'][0]['hourly_cost']='99999'
        self.assertEqual(e.calculate(self.m)['service_cost'],'33620.00')
    def test_releasable_part_time_share(self):
        self.m['people'][0]['costing']['periods'][0]['allocation_share']='0.5'
        self.m['people'][0]['capacity_hours_per_day']='4'
        for p in self.m['packages']:
            for a in p['allocations']:
                if a['person_id']=='fde':a['hours']=str(D(a['hours'])/2)
        r=e.calculate(self.m)
        self.assertEqual(r['service_cost'],'18860.00')
        self.assertEqual(r['labor_reservations'][0]['committed_cost'],'14400.00')
    def test_unallocated_committed_period_is_not_free(self):
        self.m['packages'][0]['allocations']=[a for a in self.m['packages'][0]['allocations'] if a['person_id']!='fde']
        r=e.calculate(self.m)
        self.assertEqual(r['service_cost'],'33620.00')
        self.assertEqual(r['labor_reservations'][0]['active_hours'],'0')
        self.assertEqual(sum(D(x['service_price_ex_tax']) for x in r['quote_items']),D(self.m['pricing']['fixed_price']))
    def test_outside_period_requires_explicit_policy(self):
        del self.m['people'][0]['costing']['outside_period_hourly_cost']
        with self.assertRaisesRegex(e.ModelError,'outside cost periods'):e.calculate(self.m)
    def test_overlapping_periods_rejected(self):
        period=copy.deepcopy(self.m['people'][0]['costing']['periods'][0]);period['id']='overlap'
        self.m['people'][0]['costing']['periods'].append(period)
        with self.assertRaisesRegex(e.ModelError,'overlap'):e.calculate(self.m)
    def test_fixed_vs_margin_and_client_api(self):
        self.m['pricing'].update(method='gross_margin',rate='0.25')
        r=e.calculate(self.m)
        self.assertEqual(r['service_price_ex_tax'],'44826.67')
        self.m['expenses'][2]['amount']='50000'
        self.m['expenses'][2]['api']['budget']='50000'
        self.assertEqual(e.calculate(self.m)['service_price_ex_tax'],'44826.67')
    def test_unknown_vendor_service_cost_not_zero(self):
        self.m['expenses'][3]['payer']='vendor'
        with self.assertRaisesRegex(e.ModelError,'unknown amount'):e.calculate(self.m)
    def test_reservation_csv_and_recalculation(self):
        with tempfile.TemporaryDirectory() as td:
            t=Path(td);model=t/'input.json';e.write_json(model,self.m)
            e.run(model,t/'v1')
            self.assertIn('28800.00',(t/'v1/labor-reservations.csv').read_text(encoding='utf-8'))
            self.assertTrue(e.check(t/'v1'))
    def test_previous_v1_result_fields_remain_readable(self):
        with tempfile.TemporaryDirectory() as td:
            t=Path(td);model=t/'input.json';e.write_json(model,self.m)
            v=t/'v1';e.run(model,v)
            old=e.read_json(v/'results.json')
            for key in ('labor_reservations','api_usage_details','unquoted_expenses'):old.pop(key)
            old['public_facts'].pop('public_api_basis_table')
            for row in old['workload']:row.pop('cost_method')
            e.write_json(v/'results.json',old)
            manifest=e.read_json(v/'manifest.json');manifest['files']['results.json']=e.sha(v/'results.json')
            e.write_json(v/'manifest.json',manifest)
            self.assertTrue(e.check(v))
    def test_api_basis_reaches_public_output(self):
        m=e.read_json(ROOT/'assets/example-model.json')
        r=e.calculate(m)
        self.assertIn(m['expenses'][1]['api']['usage_basis'],r['public_facts']['public_api_basis_table'])
        self.assertEqual(r['api_usage_details'][0]['usage_status'],'estimated')

class CollaborativeTests(unittest.TestCase):
    def setUp(self):
        self.m=e.read_json(ROOT/'assets/example-model.json')
    def reject(self, mutate, pattern):
        mutate(self.m)
        with self.assertRaisesRegex(e.ModelError,pattern):e.validate(self.m)
    def test_new_examples_and_activity_output(self):
        for name in ('example-model.json','reserved-period-example.json'):
            m=e.read_json(ROOT/'assets'/name);r=e.calculate(m)
            self.assertEqual(r['estimation_profile'],'ai_collaborative_v1')
            self.assertEqual(sum(D(x['hours']) for x in r['effort_details']),sum(D(x['hours']) for x in r['workload']))
            self.assertTrue(r['agent_work_details']);self.assertTrue(r['api_request_groups'])
    def test_new_profile_effort_change_does_not_discount_salary(self):
        m=e.read_json(ROOT/'assets/reserved-period-example.json')
        before=e.calculate(m)
        m['packages'][0]['human_effort'][0]['unit_hours']='2'
        m['packages'][0]['allocations'][0]['hours']='3'
        after=e.calculate(m)
        self.assertEqual(after['service_cost'],before['service_cost'])
        self.assertEqual(D(before['person_hours']['vendor'])-D(after['person_hours']['vendor']),D('4'))
    def test_new_profile_changed_version_retains_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);model=root/'model.json';e.write_json(model,self.m);e.run(model,root/'v1')
            self.m['project']['version']='v2'
            self.m['project']['change_reason']='Explicit cost update only'
            self.m['people'][0]['hourly_cost']='220'
            e.write_json(model,self.m);e.run(model,root/'v2',root/'v1')
            self.assertTrue(e.check(root/'v1'));self.assertTrue(e.check(root/'v2'))
            self.assertEqual(e.read_json(root/'v1/results.json')['effort_details'],e.read_json(root/'v2/results.json')['effort_details'])
            self.assertIn('service_cost',e.read_json(root/'v2/changes.json')['result_changes'])
    def test_automated_regression_not_per_sample_manual(self):
        r=e.calculate(e.read_json(ROOT/'assets/reserved-period-example.json'))
        qa=[h for h in r['effort_details'] if h['person_id']=='qa']
        self.assertEqual([D(x['hours']) for x in qa],[D('4'),D('2'),D('1.50'),D('.5')])
        self.assertEqual(sum(D(x['hours']) for x in qa),D('8'))
    def test_human_hours_cannot_be_unexplained(self):
        self.reject(lambda m:m['packages'][0]['human_effort'][0].update(unit_hours='3'),'each person')
    def test_totals_cannot_hide_wrong_person(self):
        self.reject(lambda m:m['packages'][0]['human_effort'][0].update(person_id='qa'),'each person')
    def test_missing_human_activities(self):
        self.reject(lambda m:m['packages'][0].pop('human_effort'),'human_effort')
    def test_agent_review_must_be_counted(self):
        self.reject(lambda m:m['packages'][0]['agent_work'][0].update(review_effort_ids=['H1']),'counted reviewer')
    def test_agent_reviewer_must_match_effort(self):
        self.reject(lambda m:m['packages'][0]['agent_work'][0].update(reviewer='qa'),'counted reviewer')
    def test_dependency_evidence_exact(self):
        self.reject(lambda m:m['packages'][1].update(dependency_basis=[]),'cover depends_on')
    def test_resource_queue_is_not_dependency_kind(self):
        self.reject(lambda m:m['packages'][1]['dependency_basis'][0].update(kind='resource'),'dependency_basis.kind')
    def test_parallel_independent_packages_allowed(self):
        # Remove a declared edge and its evidence; resource usage alone need not invent an edge.
        self.m['packages'][2].update(depends_on=[],dependency_basis=[])
        e.validate(self.m)
    def test_agent_runtime_requires_work(self):
        self.reject(lambda m:m['packages'][0].update(agent_work=[]),'agent_work and agent_hours')
    def test_api_requires_request_plan(self):
        self.reject(lambda m:m['expenses'][1]['api'].pop('request_groups'),'request_groups')
    def test_api_tokens_not_arbitrary_budget_ratio(self):
        self.reject(lambda m:m['expenses'][1]['api']['lines'][0].update(quantity_million_tokens='6'),'token quantities')
    def test_api_context_change_requires_recalculation(self):
        self.reject(lambda m:m['expenses'][1]['api']['request_groups'][0]['context_components'][0].update(tokens=3000),'token quantities')
    def test_api_tasks_must_match_expense(self):
        self.reject(lambda m:m['expenses'][1]['api']['request_groups'][0].update(agent_work_refs=['P1:A1']),'expense.task_ids')
    def test_api_unknown_agent_rejected(self):
        self.reject(lambda m:m['expenses'][1]['api']['request_groups'][0].update(agent_work_refs=['P2:missing']),'unknown reference')
    def test_api_buffer_explained(self):
        self.reject(lambda m:m['expenses'][1]['api'].pop('buffer_basis'),'buffer_basis')
    def test_new_evidence_survives_run_and_check(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);e.write_json(root/'model.json',self.m);e.run(root/'model.json',root/'v1')
            self.assertTrue((root/'v1/activity-workload.csv').exists())
            self.assertIn('context_components',(root/'v1/collaboration-evidence.json').read_text(encoding='utf-8'))
            self.assertTrue(e.check(root/'v1'))
    def test_cli_legacy_is_explicit(self):
        import subprocess,sys
        self.m.pop('estimation_profile')
        for p in self.m['packages']:
            for k in ('human_effort','agent_work','dependency_basis'):p.pop(k)
        with tempfile.TemporaryDirectory() as td:
            model=Path(td)/'model.json';e.write_json(model,self.m)
            cmd=[sys.executable,str(ROOT/'scripts/estimate.py'),'validate','--model',str(model)]
            denied=subprocess.run(cmd,capture_output=True,text=True, encoding='utf-8')
            self.assertNotEqual(denied.returncode,0);self.assertIn('--allow-legacy',denied.stderr)
            self.assertEqual(subprocess.run(cmd+['--allow-legacy'],capture_output=True).returncode,0)
            e.run(model,Path(td)/'old');self.assertTrue(e.check(Path(td)/'old'))

if __name__=='__main__': unittest.main(verbosity=2)
