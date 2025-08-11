# src/aigym/cli.py
from __future__ import annotations
import argparse, sys, pathlib, json
try:
    import yaml  # type: ignore
except Exception:
    yaml = None

ROOT = pathlib.Path(__file__).resolve().parents[2]  # repo root if editable install

def cmd_demo(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.manifest)
    if not path.exists():
        print(f"[demo] manifest not found: {path}", file=sys.stderr)
        return 2
    if yaml is None:
        print("[demo] PyYAML not installed: pip install pyyaml", file=sys.stderr)
        return 2
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    agent = data.get("agent", {}).get("name", "unknown")
    intents = data.get("agent", {}).get("handshake", {}).get("intents", [])
    tasks = [t.get("id") for t in data.get("tasks", [])]
    print(json.dumps({"agent": agent, "intents": intents, "tasks": tasks}, indent=2))
    return 0

def cmd_validate(args: argparse.Namespace) -> int:
    import json
    from importlib import resources
    from jsonschema import Draft202012Validator
    p = pathlib.Path(args.manifest)
    if not p.exists():
        print(f"[validate] file not found: {p}", file=sys.stderr)
        return 2
    if yaml is None:
        print("[validate] PyYAML not installed: pip install pyyaml", file=sys.stderr)
        return 2

    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    schema_text = resources.files("aigym").joinpath("schema/manifest.schema.json").read_text(encoding="utf-8")
    schema = json.loads(schema_text)

    v = Draft202012Validator(schema)
    errs = sorted(v.iter_errors(data), key=lambda e: (list(e.path), e.message))
    if errs:
        for e in errs:
            loc = "/" + "/".join(map(str, e.path)) if e.path else "<root>"
            print(f"[validate] {loc}: {e.message}", file=sys.stderr)
        return 1

    print("[validate] OK")
    return 0


def cmd_calibrate_pair(args: argparse.Namespace) -> int:
    # Stub so help works; wire real logic later.
    print("[calibrate-pair] baseline:", args.baseline)
    print("[calibrate-pair] left    :", args.left)
    print("[calibrate-pair] right   :", args.right)
    print("[calibrate-pair] (stub) compute priorities here")
    return 0

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="aigym", description="AIGYM CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("demo", help="Load a manifest and print summary")
    d.add_argument("manifest", help="Path to YAML manifest")
    d.set_defaults(func=cmd_demo)

    v = sub.add_parser("validate", help="YAML structure smoke-check")
    v.add_argument("manifest", help="Path to YAML manifest")
    v.set_defaults(func=cmd_validate)

    c = sub.add_parser("calibrate-pair", help="APM anti-saturation calibration (stub)")
    c.add_argument("--baseline", required=False, default="auto")
    c.add_argument("--left", required=True)
    c.add_argument("--right", required=True)
    c.set_defaults(func=cmd_calibrate_pair)

    return p

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
