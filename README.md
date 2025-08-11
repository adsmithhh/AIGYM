# AIGYM — where AI models meet, handshake, and learn to work together

> If AI models can train together, they can grow together.

AIGYM is an **open handshake & interoperability protocol** for **AI ↔ AI** interaction.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


- **Manifest** (YAML/JSON): who I am, how I work, what I need.
- **Validation CLI**: check structure/semantics.
- **Comparison**: tasks/adapters overlap.
- **APM calibration**: anti-saturation priority scaling before cooperation.
  
![CI](https://github.com/adsmithhh/AIGYM/actions/workflows/ci.yml/badge.svg)

### Quick Start (macOS/Linux or Git Bash)
```bash
pip install -e .
pip install pyyaml
aigym validate examples/agent_min.yaml
aigym demo examples/agent_min.yaml

## Quick Start
```powershell
git clone https://github.com/adsmithhh/AIGYM.git
cd AIGYM
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e .

aigym validate examples/manifest/minimal.yaml
aigym compare  examples/manifest/minimal.yaml examples/manifest/transformer.yaml
aigym calibrate --baseline configs/apm/baseline.yaml --left examples/manifest/minimal.yaml --right examples/manifest/transformer.yaml --out runs/calibration.json
``` 
## License
MIT — see [LICENSE](LICENSE).
