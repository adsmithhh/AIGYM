import json, pathlib
import yaml, jsonschema
from importlib import resources as pkgres  # stdlib in Python 3.10+

def _load(path):
    p = pathlib.Path(path)
    with open(p, "r", encoding="utf-8") as f:
        if p.suffix.lower() in [".yaml", ".yml"]:
            return yaml.safe_load(f)
        return json.load(f)

def _load_schema():
    # Try to read schema bundled in the package (works for wheels and editable installs with package-data)
    try:
        with pkgres.files("aigym.schema").joinpath("manifest.schema.json").open("r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        # Fallback for editable installs / weird paths
        schema_path = pathlib.Path(__file__).parent / "schema" / "manifest.schema.json"
        with open(schema_path, "r", encoding="utf-8-sig") as f:
            return json.load(f)

def validate_manifest(path, strict=False):
    data = _load(path)
    schema = _load_schema()

    report = {"file": str(path), "errors": [], "warnings": []}
    try:
        jsonschema.validate(instance=data, schema=schema)
        ok = True
    except jsonschema.ValidationError as e:
        ok = False
        report["errors"].append({"path": list(e.path), "message": e.message})

    if "aigym_version" not in data:
        ok = False
        report["errors"].append({"path": ["aigym_version"], "message": "missing"})

    exposure = data.get("interop", {}).get("weights", {}).get("exposure")
    if exposure not in {None, "summary", "hash", "partial", "full"}:
        report["warnings"].append({"path": ["interop","weights","exposure"], "message": "non-standard value"})

    if strict and report["warnings"]:
        ok = False

    return ok, report
