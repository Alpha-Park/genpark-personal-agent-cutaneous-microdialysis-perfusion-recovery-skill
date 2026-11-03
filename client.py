"""
Cutaneous Microdialysis Perfusion & Zero-Net-Flux (ZNF) Recovery Client.
Zero-mock pure Python standard library implementation.
Calculates microdialysis in vivo probe extraction fraction, relative recovery (RR),
and interstitial extracellular fluid (ECF) concentration via linear regression of net flux.
"""

import math
from typing import Dict, Any, List, Optional, Tuple


class CutaneousMicrodialysisClient:
    """
    Computes in vivo probe relative recovery (RR) and true extracellular tissue concentration (C_interstitial)
    using the Bungay transport model and the zero-net-flux (ZNF / no-net-flux) method.
    """

    def __init__(self, membrane_length_mm: float = 10.0, membrane_cutoff_kda: float = 20.0):
        if membrane_length_mm <= 0 or membrane_cutoff_kda <= 0:
            raise ValueError("Membrane dimensions and cutoff must be positive.")
        self.membrane_length_mm = membrane_length_mm
        self.membrane_cutoff_kda = membrane_cutoff_kda

    def calculate_relative_recovery(
        self,
        dialysate_conc_umol_l: float,
        perfusate_conc_umol_l: float = 0.0,
        known_true_tissue_conc_umol_l: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates simple relative recovery (RR) for traditional gain microdialysis (perfusate conc = 0).
        RR = C_dialysate / C_tissue * 100%
        """
        if dialysate_conc_umol_l < 0:
            raise ValueError("Dialysate concentration must be non-negative.")

        rr_pct = None
        if known_true_tissue_conc_umol_l and known_true_tissue_conc_umol_l > 0:
            rr_pct = (dialysate_conc_umol_l / known_true_tissue_conc_umol_l) * 100.0

        return {
            "status": "success",
            "dialysate_conc_umol_l": dialysate_conc_umol_l,
            "perfusate_conc_umol_l": perfusate_conc_umol_l,
            "relative_recovery_pct": round(rr_pct, 2) if rr_pct is not None else None
        }

    def zero_net_flux_calibration(
        self,
        trials: List[Tuple[float, float]],
        analyte_name: str = "Metabolite / Biomarker"
    ) -> Dict[str, Any]:
        """
        Performs in vivo Zero-Net-Flux (no-net-flux) linear regression:
        Net Flux: Delta C = C_in - C_out
        Linear equation: (C_in - C_out) = Slope * C_in + Intercept
        At Delta C = 0 (no net exchange across membrane), C_in = C_interstitial = -Intercept / Slope.
        Extraction Fraction (in vivo Recovery) = Slope.
        trials: List of (C_in, C_out) pairs in umol/L.
        """
        if not trials or len(trials) < 3:
            raise ValueError("Zero-net-flux calibration requires at least 3 distinct perfusate concentration trials.")

        # Compute net flux (Delta C = C_in - C_out) for each trial
        x_pts = []
        y_pts = []
        for c_in, c_out in trials:
            if c_in < 0 or c_out < 0:
                raise ValueError("Concentrations must be non-negative.")
            net_flux = c_in - c_out
            x_pts.append(c_in)
            y_pts.append(net_flux)

        n = len(x_pts)
        mean_x = sum(x_pts) / n
        mean_y = sum(y_pts) / n

        ss_xx = sum((x - mean_x) ** 2 for x in x_pts)
        ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_pts, y_pts))

        if ss_xx == 0:
            raise ValueError("Perfusate concentrations must vary across trials.")

        slope = ss_xy / ss_xx
        intercept = mean_y - slope * mean_x

        # Calculate Pearson R^2
        ss_yy = sum((y - mean_y) ** 2 for y in y_pts)
        r_squared = (ss_xy ** 2) / (ss_xx * ss_yy) if ss_yy > 0 else 1.0

        # In vivo Extraction Fraction / Recovery = slope
        # True interstitial concentration C_ecf = -intercept / slope (point where net flux = 0)
        if abs(slope) < 1e-6:
            raise ValueError("Slope near zero; probe transport is decoupled from tissue gradient.")

        c_interstitial_umol_l = -intercept / slope
        in_vivo_extraction_fraction = slope

        # Evaluation
        if in_vivo_extraction_fraction < 0.10:
            exchange_efficiency = "Low Extraction Efficiency / High Perfusion Flow"
            recommendation = "Consider reducing perfusion flow rate or extending membrane length."
        elif in_vivo_extraction_fraction <= 0.40:
            exchange_efficiency = "Optimal Microdialysis Recovery Profile"
            recommendation = "Membrane pore diffusion and convective balance within expected physiological range."
        else:
            exchange_efficiency = "High Extraction Efficiency / Near Equilibrium"
            recommendation = "Dialysate approximates true interstitial equilibrium."

        return {
            "status": "success",
            "analyte": analyte_name,
            "trials_analyzed": n,
            "true_interstitial_conc_umol_l": round(c_interstitial_umol_l, 2),
            "in_vivo_extraction_fraction": round(in_vivo_extraction_fraction, 4),
            "extraction_percentage": round(in_vivo_extraction_fraction * 100.0, 1),
            "linear_regression": {
                "slope": round(slope, 4),
                "intercept": round(intercept, 4),
                "r_squared": round(r_squared, 4)
            },
            "evaluation": {
                "exchange_efficiency": exchange_efficiency,
                "recommendation": recommendation,
                "membrane_cutoff_kda": self.membrane_cutoff_kda
            }
        }
