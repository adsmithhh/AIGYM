import json, sys, argparse, glob
from .validate import validate_manifest
from .compare import compare_manifests
from .calibrate import calibrate_pair
from . import db as dbmod

def main():
    p = argparse.ArgumentParser("aigym")
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Validate a manifest file")
    v.add_argument("manifest")
    v.add_argument("--strict", action="store_true")

    c = sub.add_parser("compare", help="Compare two manifests")
    c.add_argument("left")
    c.add_argument("right")
    c.add_argument("--report", default=None)

    a = sub.add_parser("calibrate", help="Calibrate priority between two manifests")
    a.add_argument("--baseline", required=True)
    a.add_argument("--left", required=True)
    a.add_argument("--right", required=True)
    a.add_argument("--out", default=None)
    a.add_argument("--sqlite", default=None, help="optional path to sqlite DB to store the calibration report")

    g = sub.add_parser("ingest", help="Ingest manifest(s) into sqlite")
    g.add_argument("--sqlite", required=True)
    g.add_argument("manifests", nargs="+", help="manifest files or globs (e.g., examples/manifest/*.yaml)")

    s = sub.add_parser("dbshow", help="Show recent rows from sqlite")
    s.add_argument("--sqlite", required=True)
    s.add_argument("--limit", type=int, default=10)

    args = p.parse_args()

    if args.cmd == "validate":
        ok, report = validate_manifest(args.manifest, strict=args.strict)
        print(json.dumps(report, indent=2))
        sys.exit(0 if ok else 2)

    if args.cmd == "compare":
        report = compare_manifests(args.left, args.right)
        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
        print(json.dumps(report, indent=2))
        return

    if args.cmd == "calibrate":
        report = calibrate_pair(args.baseline, args.left, args.right)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
        print(json.dumps(report, indent=2))
        if args.sqlite:
            dbmod.insert_calibration_report(args.sqlite, report)
        return

    if args.cmd == "ingest":
        paths = []
        for pat in args.manifests:
            paths.extend(glob.glob(pat))
        if not paths:
            print("No manifests matched.", file=sys.stderr)
            sys.exit(2)
        for mf in paths:
            dbmod.insert_manifest(args.sqlite, mf)
        print(f"Ingested {len(paths)} manifest(s) into {args.sqlite}.")
        return

    if args.cmd == "dbshow":
        summary = dbmod.recent_summary(args.sqlite, limit=args.limit)
        print(json.dumps(summary, indent=2))
        return
