#!/usr/bin/env python3
"""Small question ledger. No model calls; init refuses overwrite; ask caps at 20."""
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, value, new=False):
    data = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    if new:
        with path.open('x', encoding='utf-8') as stream:
            stream.write(data)
    else:
        tmp = path.with_name(path.name + '.tmp')
        tmp.write_text(data, encoding='utf-8')
        os.replace(tmp, path)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--state', type=Path, required=True)
    sub = p.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--project', required=True)
    ask = sub.add_parser('ask')
    ask.add_argument('--file', type=Path, required=True, help='UTF-8 text with actual proposed question and decision impact')
    ans = sub.add_parser('answer')
    ans.add_argument('--round', type=int, required=True)
    ans.add_argument('--file', type=Path, required=True, help='Actual user reply, not an invented answer')
    sub.add_parser('show')
    a = p.parse_args()
    try:
        if a.command == 'init':
            state = {'schema_version': 1, 'project': a.project, 'created_at': now(), 'round_limit': 20, 'questions': []}
            save(a.state, state, new=True)
        else:
            state = json.loads(a.state.read_text(encoding='utf-8'))
            if state.get('schema_version') != 1 or state.get('round_limit') != 20:
                raise ValueError('Unsupported or altered state contract; preserve the original question history')
            questions = state['questions']
            if [q['round'] for q in questions] != list(range(1, len(questions) + 1)) or len(questions) > 20:
                raise ValueError('Invalid question history')
            if a.command in ('ask', 'answer'):
                content = a.file.read_text(encoding='utf-8').strip()
                if not content:
                    raise ValueError('Question/reply file is empty')
            if a.command == 'ask':
                if len(questions) >= 20:
                    raise ValueError('20 rounds reached: deliver the conditional proposal and unresolved conditions; do not ask round 21')
                if questions and questions[-1]['answer'] is None:
                    raise ValueError('Previous question is pending; do not open a parallel questionnaire')
                questions.append({'round': len(questions)+1, 'asked_at': now(), 'question': content, 'answer': None})
                save(a.state, state)
            elif a.command == 'answer':
                if not 1 <= a.round <= len(questions):
                    raise ValueError('Unknown round')
                q = questions[a.round-1]
                if q['answer'] is not None:
                    raise ValueError('Reply already recorded; keep later corrections in decisions.md rather than overwriting evidence')
                q['answer'], q['answered_at'] = content, now()
                save(a.state, state)
        print(json.dumps(state, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        p.exit(2, f'ERROR: {exc}\n')


if __name__ == '__main__':
    main()
