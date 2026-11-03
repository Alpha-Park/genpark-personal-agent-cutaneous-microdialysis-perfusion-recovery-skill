"""
Example usage of Cutaneous Microdialysis Perfusion Recovery Skill.
Demonstrates zero-net-flux in vivo calibration to determine true extracellular glucose concentration.
"""

import json
from client import CutaneousMicrodialysisClient


def main():
    print("=== Testing Cutaneous Microdialysis Perfusion Recovery Skill ===")
    client = CutaneousMicrodialysisClient(membrane_length_mm=10.0, membrane_cutoff_kda=20.0)

    # In vivo Zero-Net-Flux trials for interstitial glucose (true tissue conc ~5.0 mmol/L = 5000 umol/L, extraction ~25%)
    # C_in = [0, 2500, 5000, 7500, 10000] umol/L
    # C_out = C_in - Extraction * (C_in - C_true)
    # For C_in=0: C_out = 0 - 0.25 * (0 - 5000) = 1250 umol/L -> Net Flux = -1250
    # For C_in=2500: C_out = 2500 - 0.25 * (2500 - 5000) = 3125 -> Net Flux = -625
    # For C_in=5000: C_out = 5000 - 0.25 * (5000 - 5000) = 5000 -> Net Flux = 0
    # For C_in=7500: C_out = 7500 - 0.25 * (7500 - 5000) = 6875 -> Net Flux = +625
    # For C_in=10000: C_out = 10000 - 0.25 * (10000 - 5000) = 8750 -> Net Flux = +1250

    trials = [
        (0.0, 1250.0),
        (2500.0, 3125.0),
        (5000.0, 5000.0),
        (7500.0, 6875.0),
        (10000.0, 8750.0)
    ]

    res = client.zero_net_flux_calibration(trials, analyte_name="Dermal Interstitial Glucose")
    print("\n[Zero-Net-Flux Calibration Result]")
    print(json.dumps(res, indent=2))

    # Assertions
    assert res["status"] == "success"
    assert abs(res["true_interstitial_conc_umol_l"] - 5000.0) < 1.0
    assert abs(res["in_vivo_extraction_fraction"] - 0.25) < 0.01
    assert res["linear_regression"]["r_squared"] > 0.999
    print("\n[SUCCESS] Cutaneous Microdialysis tests passed with perfect precision!")


if __name__ == "__main__":
    main()
