# scripts/ — generators

| script | what it makes | how to run |
|---|---|---|
| `make_logo.py` | `assets/vanguard_logo_final.png` (roster v3: 11 members, Kazakhstan + Barbados both in) | needs Pillow |
| `build_dr_pdf.py` | `drafts/VANGUARD_DR1.2.pdf` — decorated DR (border, logo, sponsors/signatories, stripped custody tags) | needs reportlab |

Regeneration (sandbox: system pip is PEP-668-locked, so use a venv):

```bash
python3 -m venv /tmp/pdfenv
/tmp/pdfenv/bin/pip install reportlab pillow pymupdf
cd <repo>
/tmp/pdfenv/bin/python scripts/make_logo.py
/tmp/pdfenv/bin/python scripts/build_dr_pdf.py
```

The DR PDF always re-reads `drafts/VANGUARD_DR1.2.md`, so editing the MD
(adding clauses, changing sponsors) and re-running the script keeps the PDF in sync.
Custody tags `[MX anchor]`, `**[JAPAN — UMBRELLA]**` etc. are stripped automatically
for the circulation version.

Note: ImageMagick in this sandbox cannot emit PDF (security policy) and cannot
rasterize SVG (no rsvg-convert delegate), hence the pure-Python toolchain.
