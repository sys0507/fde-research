#!/usr/bin/env python3
"""Build a deterministic, self-contained skill ZIP or install a fresh copy."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile
import check_package

ROOT = Path(__file__).resolve().parents[1]


def manifest(root):
    data = json.loads((root / 'release-manifest.json').read_text(encoding='utf-8'))
    names = data['files']
    if len(names) != len(set(names)):
        raise ValueError('Duplicate manifest entries')
    for name in names:
        path = root / name
        if Path(name).is_absolute() or '..' in Path(name).parts or '\\' in name:
            raise ValueError('Unsafe manifest path: ' + name)
        if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink() or not path.is_file():
            raise ValueError('Missing or unsafe file: ' + name)
    return data


def copy_payload(root, target):
    data = manifest(root)
    target.mkdir(parents=True, exist_ok=False)
    for name in data['files']:
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / name, destination)
    return data


def install(root, destination):
    destination = destination.expanduser().resolve()
    if destination.name != 'fde-research':
        raise ValueError('Installation folder must be named fde-research')
    if destination.exists():
        raise FileExistsError('Existing installation preserved: ' + str(destination))
    if destination.is_relative_to(root.resolve()):
        raise ValueError('Install outside the source repository')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.fde-install-', dir=destination.parent) as temp:
        staged = Path(temp) / 'fde-research'
        copy_payload(root, staged)
        report = check_package.check(staged, installed=True)
        if not report['passed']:
            raise ValueError(report['errors'])
        staged.rename(destination)
    return destination


def build(root, output):
    output = output.expanduser().resolve()
    if output.is_relative_to(root.resolve()):
        raise ValueError('Release output must be outside the repository')
    data = manifest(root)
    report = check_package.check(root)
    if not report['passed']:
        raise ValueError(report['errors'])
    output.mkdir(parents=True, exist_ok=True)
    archive = output / ('fde-research-' + data['edition'] + '-v' + data['version'] + '.zip')
    checksum = archive.with_suffix('.zip.sha256')
    if archive.exists() or checksum.exists():
        raise FileExistsError('Release files already exist; choose a fresh output directory')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as bundle:
        for name in sorted(data['files']):
            info = zipfile.ZipInfo('fde-research/' + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, (root / name).read_bytes())
    checksum.write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n', encoding='utf-8')
    return archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path)
    group.add_argument('--install', type=Path, metavar='DESTINATION')
    args = parser.parse_args()
    print(build(ROOT, args.output) if args.output else install(ROOT, args.install))


if __name__ == '__main__':
    main()
