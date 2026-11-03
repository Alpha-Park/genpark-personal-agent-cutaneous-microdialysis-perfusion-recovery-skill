---
name: genpark-personal-agent-cutaneous-microdialysis-perfusion-recovery-skill
description: Cutaneous Microdialysis Relative Recovery (RR) and interstitial molecular flux analyzer. Computes zero-net-flux (ZNF) in vivo calibration, no-net-flux point, and extracellular interstitial drug/metabolite concentrations based on Taylor dispersion and Bungay diffusion models.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - dermatology
  - microdialysis
  - interstitial-fluid
  - zero-net-flux
  - openclaw
  - genpark
  - mcp
---

# Cutaneous Microdialysis Perfusion Recovery Skill

## Overview
This skill computes true extracellular fluid ($C_{\text{ecf}}$) concentrations of dermal interstitial biomarkers (e.g., glucose, lactate, histamine, cytokines) without requiring prior in vitro calibration:
- **Zero-Net-Flux (ZNF) Method**: Perfusate containing varying analyte concentrations ($C_{\text{in}}$) is perfused through a semi-permeable capillary fiber.
- **Linear Net Flux Equation**: Net exchange $\Delta C = C_{\text{in}} - C_{\text{out}}$ is plotted against $C_{\text{in}}$.
- **No-Net-Exchange Point**: The x-intercept where $\Delta C = 0$ represents the point where perfusate is in thermodynamic equilibrium with tissue interstitial fluid ($C_{\text{in}} = C_{\text{ecf}}$).
- **In Vivo Extraction Fraction**: The slope of the regression line equals the in vivo extraction fraction ($E_d$).

## Mathematical Formulation
1. **Net Membrane Flux**:
   $$\Delta C = C_{\text{in}} - C_{\text{out}}$$
2. **Linear Regression Model**:
   $$\Delta C = E_d \cdot C_{\text{in}} - E_d \cdot C_{\text{ecf}}$$
3. **True Extracellular Concentration**:
   $$C_{\text{ecf}} = -\frac{\text{Intercept}}{\text{Slope}}$$
4. **In Vivo Extraction Fraction**:
   $$\text{Recovery Fraction } (E_d) = \text{Slope}$$

## Usage
```python
from client import CutaneousMicrodialysisClient

client = CutaneousMicrodialysisClient()
res = client.zero_net_flux_calibration(
    trials=[(0.0, 1250.0), (2500.0, 3125.0), (5000.0, 5000.0), (7500.0, 6875.0)]
)
print(res["true_interstitial_conc_umol_l"])
```
