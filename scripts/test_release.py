import json
from pathlib import Path
import tempfile
import unittest
import zipfile
import release_package as release
import check_package


class ReleaseTests(unittest.TestCase):
    def test_manifest_covers_payload_and_excludes_repository_metadata(self):
        data = release.manifest(release.ROOT)
        actual = {p.relative_to(release.ROOT).as_posix() for p in check_package.package_files(release.ROOT)[0]}
        self.assertEqual(set(data['files']), actual)
        self.assertFalse(any(p.startswith(('.git/', '.github/', 'validation/')) for p in actual))

    def test_zip_is_deterministic_and_independently_valid(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = release.build(release.ROOT, root / 'first')
            second = release.build(release.ROOT, root / 'second')
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as bundle:
                bundle.extractall(root / 'unpacked')
            report = check_package.check(root / 'unpacked/fde-research', installed=True)
            self.assertTrue(report['passed'], report['errors'])

    def test_install_preserves_existing_target(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'fde-research'
            release.install(release.ROOT, target)
            marker = target / 'README.md'
            before = marker.read_bytes()
            with self.assertRaises(FileExistsError):
                release.install(release.ROOT, target)
            self.assertEqual(before, marker.read_bytes())

    def test_unsafe_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'release-manifest.json').write_text(json.dumps({'files': ['../outside']}), encoding='utf-8')
            with self.assertRaises(ValueError):
                release.manifest(root)


if __name__ == '__main__':
    unittest.main()
