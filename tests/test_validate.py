from aigym.validate import validate_manifest

def test_minimal_manifest_valid():
    ok, report = validate_manifest("examples/manifest/minimal.yaml", strict=False)
    assert ok, report
    assert report["errors"] == []
