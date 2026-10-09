# Historical Linux rendering evidence: independent edition copy

This directory contains only the English 2.2.1 cases and review images. Raw DOCX/PDF/log/PNG artifacts are unchanged. The summary is an edition-only extract retaining correction provenance and the original summary hash. No render was repeated; this is not evidence that 2.3.0 passed on all platforms. The original summary read `pages` instead of `page_count`; this was corrected afterward. Both successful cases have six pages and two rendering passes.

Environment: Python 3.13.16, LibreOffice 24.2.7.2, Linux. A matches installed fonts; B accepts actual substitution. Both still require visual review. Absolute paths in raw logs describe the historical environment and are not runtime dependencies.

Run `python -B verify_evidence.py` with Pillow installed. Non-PNG files use byte hashes; PNGs use decoded RGB pixels and dimensions because transfer embedded C2PA metadata. Equal pixels do not imply equal PNG bytes. Manifests are scoped to this repository; the byte manifest does not hash itself. The historical package manifest identifies the old source, not an expectation that the current package is unchanged. The current repeatable smoke runner is `scripts/smoke_word.py` at repository root.
