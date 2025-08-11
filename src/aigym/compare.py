# src/aigym/compare.py
from .validate import _load

def _task_names(M):
    tasks = (M.get("capabilities") or {}).get("tasks") or []
    return [t["name"] for t in tasks if isinstance(t, dict) and t.get("name")]

def _adapter_key(a):
    if not isinstance(a, dict):
        return ("", tuple(), None)
    return (a.get("type"), tuple(a.get("scope") or []), a.get("rank"))

def _adapters(M):
    return set(_adapter_key(a) for a in (M.get("adapters") or []))

def _as_list(items):
    return [[t, list(scope), rank] for (t, scope, rank) in items]

def compare_manifests(left_path, right_path):
    L = _load(left_path)
    R = _load(right_path)

    left_id  = (L.get("model") or {}).get("id")
    right_id = (R.get("model") or {}).get("id")

    L_tasks = set(_task_names(L))
    R_tasks = set(_task_names(R))

    L_ad = _adapters(L)
    R_ad = _adapters(R)

    return {
        "left": left_id,
        "right": right_id,
        "task_overlap": sorted(L_tasks & R_tasks),
        "task_left_only": sorted(L_tasks - R_tasks),
        "task_right_only": sorted(R_tasks - L_tasks),
        "adapter_overlap": _as_list(sorted(L_ad & R_ad)),
        "adapter_left_only": _as_list(sorted(L_ad - R_ad)),
        "adapter_right_only": _as_list(sorted(R_ad - L_ad)),
    }
