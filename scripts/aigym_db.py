# scripts/aigym_db.py
import sqlite3, json, pathlib, datetime
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB   = ROOT / "aigym.db"

def connect():
    con = sqlite3.connect(DB)
    # row factory for nicer prints
    con.row_factory = sqlite3.Row
    return con

def init_schema(con):
    con.executescript("""
    CREATE TABLE IF NOT EXISTS manifest (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name  TEXT,
        body        TEXT NOT NULL,                     -- JSON as text
        created_at  TEXT DEFAULT (datetime('now'))     -- ISO timestamp
    );

    CREATE TABLE IF NOT EXISTS calibration (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        left_model  TEXT,
        right_model TEXT,
        report      TEXT NOT NULL,                     -- JSON as text
        created_at  TEXT DEFAULT (datetime('now'))
    );
    """)
    con.commit()

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def upsert_examples(con):
    # insert example manifests if they exist
    examples = [
        ROOT / "examples" / "manifest" / "minimal.yaml",
        ROOT / "examples" / "manifest" / "transformer.yaml",
    ]
    for p in examples:
        if p.exists():
            data = load_yaml(p)
            model_name = data.get("model", {}).get("id")
            con.execute(
                "INSERT INTO manifest (model_name, body) VALUES (?, ?)",
                (model_name, json.dumps(data, ensure_ascii=False)),
            )
    con.commit()

def ingest_calibration(con):
    # optional: insert the last calibration run if present
    cal = ROOT / "runs" / "calibration.json"
    if cal.exists():
        with open(cal, "r", encoding="utf-8") as f:
            rep = json.load(f)
        con.execute(
            "INSERT INTO calibration (left_model, right_model, report) VALUES (?, ?, ?)",
            (rep.get("left"), rep.get("right"), json.dumps(rep, ensure_ascii=False)),
        )
        con.commit()

def demo_query(con):
    # SQLite json1 operators: use json_extract to access JSON
    sql = """
    SELECT
        model_name,
        json_extract(body, '$.model.id')              AS id_from_json,
        json_extract(body, '$.interop.weights.exposure') AS exposure
    FROM manifest
    WHERE json_extract(body, '$.interop.weights.exposure') = 'summary';
    """
    rows = list(con.execute(sql))
    print(f"\nManifests with exposure='summary' ({len(rows)}):")
    for r in rows:
        print(f" - {r['model_name']}  (id_from_json={r['id_from_json']})")

if __name__ == "__main__":
    con = connect()
    init_schema(con)
    upsert_examples(con)
    ingest_calibration(con)
    demo_query(con)
    print(f"\nSQLite DB ready at: {DB}")
