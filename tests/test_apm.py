import yaml, tempfile, os
from aigym.calibrate import calibrate_pair

def test_calibrate_clipping_and_sum_to_one(tmp_path):
    # Floor/ceiling will force clip to 0.4/0.6 then renormalize (sum=1)
    baseline = tmp_path / "baseline.yaml"
    baseline.write_text(yaml.safe_dump({
        "apm_version": "0.1.0",
        "priority": {"floor": 0.4, "ceiling": 0.6},
    }), encoding="utf-8")

    rep = calibrate_pair(
        str(baseline),
        "examples/manifest/minimal.yaml",
        "examples/manifest/transformer.yaml",
    )
    pL = rep["priority_allocation"]["left"]
    pR = rep["priority_allocation"]["right"]
    assert abs((pL + pR) - 1.0) < 1e-9
    # With our examples, minimal < transformer; after clipping becomes 0.4 vs 0.6
    assert pL <= 0.6 and pL >= 0.4
    assert pR <= 0.6 and pR >= 0.4
