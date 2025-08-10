# AIGYM — AI↔AI Weight-Exchange Handshake (v0.1)

A thin, interoperable protocol for exchanging adapters (LoRA, IA³) and full diffs between AI systems.
Negotiates compatibility and integrity **without exposing base weights**.

- **Headers or manifest**: online via HTTP/gRPC headers, or offline via `exchange_manifest`.
- **Integrity**: content-addressed blobs (sha256), signatures, dry-run apply, rollback pointers.
- **Telemetry**: optional adoption/dialect reporting.

## Quick start
- Read `spec/aigym-handshake.yaml` or `spec/aigym-handshake.json`.
- See `examples/manifest.example.yaml` and `examples/compat.response.json`.
- Run `tools/verify_manifest.py examples/manifest.example.yaml` (requires PyYAML).

MIT License.
