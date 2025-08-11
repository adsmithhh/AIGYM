# AIGYM – Current Status

## Done (Working Locally)

### CLI Surface
- `aigym validate <manifest>`
- `aigym compare <left> <right>`
- `aigym calibrate --baseline … --left … --right … [--out …] [--sqlite …]`
- `aigym ingest --sqlite <db> <globs…>`
- `aigym dbshow --sqlite <db> [--limit N]`
- `calibrate` now creates parent dirs for `--out` before writing.

### SQLite Integration
- `src/aigym/db.py` with tables `manifest` and `calibration`.
- CLI wiring for ingest/save/show; JSON stored verbatim.

### Schema + Validation
- `src/aigym/schema/manifest.schema.json` bundled with the package.
- Loader uses `importlib.resources` and tolerates BOM via `utf-8-sig`.
- `validate` returns structured report with errors / warnings.

### Examples & Config
- `examples/manifest/minimal.yaml`
- `examples/manifest/transformer.yaml`
- `configs/apm/baseline.yaml`

### Tests
- `tests/test_validate.py` (schema + basics)
- `tests/test_compare.py` (overlap/only sets)
- `tests/test_apm.py` (clipping + sum-to-one)
- Local: 3 passed.

### CI
- GitHub Actions matrix: `ubuntu-latest` + `windows-latest`.
- Steps: install (editable), CLI smoke (validate/compare/calibrate), pytest.

### Docs & Housekeeping
- README Quick Start (PowerShell).
- MIT license file.
- `.gitattributes` and `.gitignore` basics.
- Tags up through `v0.1.1`.

---

## Missing / Next

- Place this status documentation somewhere accessible (e.g., root `STATUS.md` or in docs).
- Expand documentation beyond Quick Start (usage, architecture, examples).
- Add more robust test coverage (edge cases, error handling).
- Improve error reporting and user feedback in CLI.
- Consider packaging and publishing (PyPI).
- Add badges to README (CI status, version, license).
- Document schema details and validation logic in docs.
- Add changelog/history file for releases/tags.