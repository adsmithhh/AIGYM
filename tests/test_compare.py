from aigym.compare import compare_manifests

def test_compare_overlap_and_only_sets():
    rep = compare_manifests("examples/manifest/minimal.yaml", "examples/manifest/transformer.yaml")
    assert "classification" in rep["task_overlap"]
    assert "generation" in rep["task_right_only"]
