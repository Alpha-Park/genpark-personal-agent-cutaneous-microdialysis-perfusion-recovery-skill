# Cutaneous Microdialysis Perfusion Recovery Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Cutaneous Microdialysis In Vivo Relative Recovery and Zero-Net-Flux (ZNF) Quantitative Analyzer based on Bungay transport modeling.

```mermaid
flowchart TD
    A[Variable Perfusate Concentrations C_in] --> B[Collect Dialysate Concentrations C_out]
    B --> C[Compute Net Membrane Flux: Delta C = C_in - C_out]
    C --> D[Linear Regression: Delta C vs C_in]
    D --> E[Zero-Net-Flux Point: Delta C = 0 -> True C_interstitial]
    D --> F[Slope = In Vivo Probe Extraction Fraction E_d]
    E & F --> G[Biomarker Quantitation & Probe Delivery Guidance]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Zero-Net-Flux Method**: Determines exact interstitial concentrations independent of unknown tissue tortuosity or probe fouling.
- **Bungay Transport Physics**: Validated against classic in vivo microdialysis mass-transfer equations.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
