# scripts/aigym_db_show.py
import sqlite3, pathlib, json
ROOT = pathlib.Path(__file__).resolve().parents[1]
DB   = ROOT / "aigym.db"

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("\nManifests:")
for r in con.execute("SELECT id, model_name, datetime(created_at) as ts FROM manifest ORDER BY id DESC LIMIT 10"):
    print(f" - #{r['id']:>3}  {r['model_name']}  @ {r['ts']}")

print("\nCalibrations:")
for r in con.execute("SELECT id, left_model, right_model, datetime(created_at) as ts FROM calibration ORDER BY id DESC LIMIT 10"):
    print(f" - #{r['id']:>3}  {r['left_model']}  vs  {r['right_model']}  @ {r['ts']}")

con.close()
print(f"\nDB: {DB}")
