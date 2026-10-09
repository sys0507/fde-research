#!/usr/bin/env python3
"""Verify this evidence folder.

Non-PNG files: byte SHA-256 against SHA256SUMS.txt.
PNG files: SHA-256 of decoded RGB pixels plus size against PIXEL-SHA256.txt, because some
file-transfer paths embed a C2PA provenance chunk (caBX) into PNGs without changing pixels.
Requires Pillow for the PNG check. Usage: python verify_evidence.py [folder]
"""
import hashlib, sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent)
bad = 0
for line in (root / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
    digest, rel = line.split('  ', 1)
    if hashlib.sha256((root / rel).read_bytes()).hexdigest() != digest:
        bad += 1; print('BYTE MISMATCH', rel)
from PIL import Image
for line in (root / 'PIXEL-SHA256.txt').read_text(encoding='utf-8').splitlines():
    digest, size, rel = line.split('  ', 2)
    with Image.open(root / rel) as im:
        rgb = im.convert('RGB')
        got = hashlib.sha256(rgb.tobytes()).hexdigest(); dims = f'{rgb.width}x{rgb.height}'
    if (got, dims) != (digest, size):
        bad += 1; print('PIXEL MISMATCH', rel)
print('OK' if bad == 0 else f'{bad} mismatches')
raise SystemExit(1 if bad else 0)
