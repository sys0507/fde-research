# Independent maintenance, validation, and release

This edition owns its version, dependencies, CI, evidence, and release archive. No checkout or coordinated release of another language is required. Current version: 2.3.0. Public visibility does not grant a reuse license; LICENSE governs rights.

Create a Python 3.12 environment outside this repository and use its interpreter to install `requirements-test.txt`. It pins direct dependencies; pip still resolves transitive dependencies, so this is not a complete environment lock. The generic Word requirements and Codex-specific path remain in skill 9. Optional screenshot capture needs Playwright and Chromium in a separate tools directory, never inside the skill package.

```sh
python -m pip install -r requirements-test.txt
python -B -X utf8 scripts/check_package.py
python -B -X utf8 scripts/run_tests.py --output ../fde-test-results
python -B -X utf8 scripts/release_package.py --output ../fde-release
```

Here `python` is the external environment interpreter on any platform. Outputs must be outside the repository. The runner includes 102 existing regressions plus four release tests. Strict encoding warnings exempt only two third-party pypdfium2 version readers. `release-manifest.json` enumerates this edition's installation files; update it after adding/removing files, or completeness tests fail. ZIPs have a single `fde-research/` root and adjacent SHA-256. Identical inputs produce identical ZIP bytes. After extraction run `scripts/check_package.py --installed`.

CI independently tests Python 3.12 on Windows/Linux, verifies evidence, and builds retained artifacts. It never pushes or creates a Release. A separate manual Linux LibreOffice workflow performs real conversion; every final page still requires human review. Workflows are configured, not claimed to have passed on GitHub before the first push. Actions use pinned commit SHAs; upgrades are explicit.

For a version change update VERSION, root SKILL metadata, release-manifest, the current README version, and CHANGELOG. Do not rewrite historical entries or evidence. See [validation](validation.md). Historical evidence lives in the repository's `validation/evidence/2.2.1-linux/` and is excluded from agent installations. Publishers need the relevant publication rights; preserved provenance is in [NOTICE](../NOTICE.md).

For the first push, create an empty GitHub repository without an initial README/license, configure its actual URL as `origin`, inspect local main and status, then push. Never embed an access token in that URL. Wait for CI; only then tag the intended release commit as `v2.3.0` and upload this repository's ZIP and `.sha256`. Preparation does not set a remote, push, create a tag, or publish a Release.
