import yaml
from .validate import _load

def _load_yaml(p):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def _cap(v, lo, hi):
    return max(lo, min(hi, v))

def calibrate_pair(baseline_path, left_path, right_path):
    B = _load_yaml(baseline_path)
    L = _load(left_path)
    R = _load(right_path)

    # crude demand score based on number of tasks and parameter count
    def demand(M):
        tasks = (M.get("capabilities") or {}).get("tasks") or []
        n_tasks = len(tasks) or 1
        params = float((M.get("model") or {}).get("parameters", 1))
        return max(1.0, n_tasks * (params ** 0.25) / 100.0)

    dL, dR = demand(L), demand(R)
    total = dL + dR
    floor = float(B["priority"]["floor"])
    ceil = float(B["priority"]["ceiling"])

    # proportional allocation, clipped to band, renormalized
    pL_raw, pR_raw = dL / total, dR / total
    pL, pR = _cap(pL_raw, floor, ceil), _cap(pR_raw, floor, ceil)
    s = pL + pR
    pL, pR = pL / s, pR / s

    return {
        "apm_version": B.get("apm_version", "0.1.0"),
        "left": (L.get("model") or {}).get("id"),
        "right": (R.get("model") or {}).get("id"),
        "priority_allocation": {"left": pL, "right": pR},
        "notes": [
            "Proportional allocation, clipped to [floor, ceiling], renormalized.",
            "Replace with your preferred control law (PID, consensus, etc)."
        ],
    }
