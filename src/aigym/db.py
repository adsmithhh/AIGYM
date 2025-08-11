# src/aigym/db.py
import sqlite3, json, yaml, pathlib

SCHEMA = """
CREATE TABLE IF NOT EXISTS manifest (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  model_name  TEXT,
  body        TEXT NOT NULL,
  created_at  TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS calibration (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  left_model  TEXT,
  right_model TEXT,
  report      TEXT NOT NULL,
  created_at  TEXT DEFAULT (datetime('now'))
);
"""

def _connect(db_path):
    p = pathlib.Path(db_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(p))
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con

def insert_manifest(db_path, manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    model_name = (data.get("model") or {}).get("id")
    con = _connect(db_path)
    con.execute(
        "INSERT INTO manifest (model_name, body) VALUES (?, ?)",
        (model_name, json.dumps(data, ensure_ascii=False)),
    )
    con.commit(); con.close()

def insert_calibration_report(db_path, report_dict):
    con = _connect(db_path)
    con.execute(
        "INSERT INTO calibration (left_model, right_model, report) VALUES (?, ?, ?)",
        (report_dict.get("left"), report_dict.get("right"), json.dumps(report_dict, ensure_ascii=False)),
    )
    con.commit(); con.close()

def recent_summary(db_path, limit=10):
    con = _connect(db_path)
    rows_m = list(con.execute(
        "SELECT id, model_name, created_at FROM manifest ORDER BY id DESC LIMIT ?", (limit,)))
    rows_c = list(con.execute(
        "SELECT id, left_model, right_model, created_at FROM calibration ORDER BY id DESC LIMIT ?", (limit,)))
    con.close()
    return {"manifests":[dict(r) for r in rows_m], "calibrations":[dict(r) for r in rows_c]}
