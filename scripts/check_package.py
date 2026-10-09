#!/usr/bin/env python3
"""Read-only package structure, source syntax and local Markdown link checks.

Does not execute skills, install tools, contact external URLs, or validate business
judgement. Optional links to the master package are checked in full-package mode.
"""
import argparse
import ast
import json
import os
from pathlib import Path
import re
import hashlib
from urllib.parse import unquote, urlsplit

EXPECTED = {
    'fde-discovery-guide', 'fde-baseline-analysis', 'fde-business-diagnosis',
    'write-business-ai-proposal', 'fde-ai-scenario-design', 'fde-prototype-development',
    'fde-implementation-readiness', 'design-ai-project-architecture', 'plan-ai-project-delivery',
}


def without_fences(text):
    lines, marker = [], None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            token = match.group(1)
            if marker is None:
                marker = token[0]
            elif token[0] == marker:
                marker = None
        elif marker is None:
            lines.append(line)
    return '\n'.join(lines)


def encoding_issues(tree):
    """Check text APIs, excluding binary modes and third-party document openers.

    This is a source lint, not whole-program type inference. An explicit encoding
    expression is allowed for customer formats; literal None is not explicit.
    """
    issues = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else func.id if isinstance(func, ast.Name) else ''
        owner = func.value.id if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) else ''
        encoding_index = None
        if name in ('read_text', 'write_text'):
            encoding_index = 0 if name == 'read_text' else 1
        elif name == 'open':
            # These read binary document/image containers, not locale text files.
            if owner in ('Image', 'pdfplumber', 'fitz', 'zipfile', 'tarfile'):
                continue
            builtin = isinstance(func, ast.Name) or owner in ('io', 'builtins')
            mode_index = 1 if builtin else 0
            mode = next((k.value for k in node.keywords if k.arg == 'mode'),
                        node.args[mode_index] if len(node.args) > mode_index else ast.Constant('r'))
            if isinstance(mode, ast.Constant) and isinstance(mode.value, str) and 'b' in mode.value:
                continue
            encoding_index = 3 if builtin else 2
        elif owner == 'subprocess' and name in ('run', 'Popen', 'check_output'):
            if any(k.arg in ('text', 'universal_newlines') and isinstance(k.value, ast.Constant)
                   and k.value.value is True for k in node.keywords):
                encoding_index = 1000  # subprocess encoding is keyword-only
        if encoding_index is None:
            continue
        value = next((k.value for k in node.keywords if k.arg == 'encoding'),
                     node.args[encoding_index] if len(node.args) > encoding_index else None)
        if value is None or isinstance(value, ast.Constant) and value.value is None:
            issues.append(f'line {node.lineno}: {name} text I/O needs an explicit encoding')
    return issues


def personal_paths(text):
    # Permit documented placeholders; reject literal machine-specific home names.
    pattern = r'(?:[A-Za-z]:[\\/]+Users[\\/]+|/(?:Users|home)/)([^\\/\s§<>"|]+)'.replace('§', chr(96))
    placeholders = {'your-user', 'your-username', 'username', 'user', '\u4f60\u7684\u7528\u6237\u540d'}
    return [m.group(0) for m in re.finditer(pattern, text, re.I)
            if m.group(1).lower() not in placeholders
            and not m.group(1).startswith(('%', '$', '{', '['))]


ENVIRONMENT_DIRS = {'.venv', 'venv', 'node_modules', 'site-packages', '__pypackages__',
                    '.tox', '.nox', '.conda'}
ENVIRONMENT_MARKERS = ('pyvenv.cfg', 'conda-meta')


def package_files(root):
    """Return package files, pruning runtime environments that must live outside it."""
    files, environments = [], []
    for current, dirs, names in os.walk(root):
        here = Path(current)
        kept = []
        for name in sorted(dirs):
            child = here / name
            if here == root and name in {'.git', '.github', 'validation'}:
                continue
            if name in ENVIRONMENT_DIRS or any((child / m).exists() for m in ENVIRONMENT_MARKERS):
                environments.append(child.relative_to(root).as_posix())
            else:
                kept.append(name)
        dirs[:] = kept
        files.extend(here / name for name in names if not (here == root and name in {'.gitignore', '.gitattributes', 'CONTRIBUTING.md', 'SECURITY.md'}))
    return sorted(p for p in files if p.is_file()), environments


def check(root, installed=False):
    root = root.resolve()
    errors, warnings, links = [], [], 0
    if root.name != 'fde-research':
        message = 'Root folder must be fde-research for installation; source workspace name may differ.'
        (errors if installed else warnings).append(message)
    actual = {p.parent.name for p in root.glob('*/SKILL.md')}
    if actual != EXPECTED:
        errors.append('Expected exactly the nine skill folders: ' + str(sorted(actual ^ EXPECTED)))
    for required in ['SKILL.md', 'README.md', 'docs/handoff-contract.md',
                     'docs/runtime-and-installation.md', 'docs/unified-entry.md', 'docs/workflow-map.md']:
        if not (root / required).is_file():
            errors.append('Missing ' + required)
    files, environments = package_files(root)
    for rel in environments:
        errors.append('Runtime environment inside package: ' + rel
                      + '/ (keep virtual environments and node_modules outside the skill package)')
    expected_manifests = {'SKILL.md'} | {name + '/SKILL.md' for name in EXPECTED}
    actual_manifests = {p.relative_to(root).as_posix() for p in files if p.name == 'SKILL.md'}
    if actual_manifests != expected_manifests:
        errors.append('Expected one root entry and nine professional skill manifests: '
                      + str(sorted(actual_manifests ^ expected_manifests)))
    entries = [(root, 'fde-research')]
    entries.extend((root / name, name) for name in sorted(EXPECTED & actual))
    for path, name in entries:
        for required in ['README.md', 'SKILL.md']:
            if not (path / required).is_file():
                errors.append('Missing ' + name + '/' + required)
        if not (path / 'SKILL.md').is_file():
            continue
        text = (path / 'SKILL.md').read_text(encoding='utf-8')
        front = re.match(r'\A---\r?\n(.*?)\r?\n---', text, re.S)
        if not front:
            errors.append(name + ': missing frontmatter')
        else:
            fields = front.group(1)
            if not re.search(r'^name:[ \t]*' + re.escape(name) + r'[ \t]*$', fields, re.M):
                errors.append(name + ': mismatched name')
            if not re.search(r'^description:[ \t]*\S', fields, re.M):
                errors.append(name + ': empty description')
    for path in files:
        rel = path.relative_to(root).as_posix()
        if '__pycache__' in path.parts or path.suffix in ('.pyc', '.pyo'):
            errors.append('Generated cache in package: ' + rel)
        try:
            if path.suffix in ('.md', '.py', '.cjs', '.json', '.yaml', '.yml', '.txt', '.html'):
                for literal in personal_paths(path.read_text(encoding='utf-8')):
                    errors.append(rel + ': personal home path: ' + literal)
            if path.suffix == '.json':
                json.loads(path.read_text(encoding='utf-8'))
            elif path.suffix == '.py':
                tree = ast.parse(path.read_text(encoding='utf-8'), filename=rel)
                errors.extend(rel + ': ' + issue for issue in encoding_issues(tree))
            elif path.suffix == '.md':
                content = without_fences(path.read_text(encoding='utf-8'))
                content = re.sub(r'`[^`\n]+`', '', content)
                for match in re.finditer(r'!?\[[^\]\n]*\]\(<?([^\s)>]+)>?\)', content):
                    target = match.group(1)
                    parsed = urlsplit(target)
                    if parsed.scheme or not parsed.path:
                        continue
                    # Template output-relative links resolve in a future project,
                    # unlike ../ references back into the package's methods.
                    if 'assets' in path.relative_to(root).parts and not parsed.path.startswith('../'):
                        continue
                    links += 1
                    linked = (path.parent / unquote(parsed.path)).resolve()
                    if not linked.is_relative_to(root):
                        errors.append(rel + ': local link leaves package: ' + target)
                    elif not linked.exists():
                        errors.append(rel + ': missing link: ' + target)
        except (ValueError, SyntaxError, OSError) as exc:
            errors.append(rel + ': ' + str(exc))
    # Explicitly shared copies preserve standalone skill installation.
    templates = sorted((root / 'fde-baseline-analysis/assets/templates').glob('*.md'))
    if len(templates) != 3:
        errors.append('Expected the three shared investigation/baseline templates')
    pairs = [(p, root / 'fde-discovery-guide/assets/templates' / p.name) for p in templates]
    pairs.append((root / 'design-ai-project-architecture/scripts/check_pdf_fonts.py',
                  root / 'plan-ai-project-delivery/scripts/check_pdf_fonts.py'))
    for left, right in pairs:
        if not left.is_file() or not right.is_file():
            errors.append('Missing shared copy: ' + str(left.relative_to(root)))
        elif hashlib.sha256(left.read_bytes()).digest() != hashlib.sha256(right.read_bytes()).digest():
            errors.append('Shared copies differ: ' + str(left.relative_to(root)) + ' / ' + str(right.relative_to(root)))
    return {'passed': not errors, 'skills': len(actual),
            'entry_skill': 'fde-research' if (root / 'SKILL.md').is_file() else None,
            'skill_manifests': sum(p.name == 'SKILL.md' for p in files), 'files': len(files),
            'local_links_checked': links, 'shared_pairs_checked': len(pairs),
            'installation_name_checked': installed, 'warnings': warnings, 'errors': errors,
            'scope': 'Static source, text-encoding, shared-copy, personal-path, runtime-environment and package checks; no project or visual validation.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--installed', action='store_true', help='Require the root directory to match name: fde-research')
    args = parser.parse_args()
    result = check(args.root.resolve(), installed=args.installed)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
