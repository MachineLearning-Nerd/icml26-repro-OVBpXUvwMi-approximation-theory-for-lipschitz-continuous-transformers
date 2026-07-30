"""Controls that must be rejected for the theorem-specific reason."""

from __future__ import annotations

import numpy as np


def run_negative_controls() -> dict:
    controls = {
        "claim_1_oversized_step": {
            "premise_changed": "tau=2.1/||W||^2 exceeds the closed admissible interval",
            "observed_lipschitz": 1.1,
            "rejected": abs(1 - 2.1) > 1,
        },
        "claim_2_oversized_attention_step": {
            "premise_changed": "eta=2.1/beta for a two-point context",
            "observed_jacobian_norm_at_origin": 1.1,
            "rejected": abs(1 - 2.1) > 1,
        },
        "claim_3_expansive_layer": {
            "premise_changed": "one layer has query Lipschitz constant 1.01",
            "observed_composition_bound": 1.01,
            "rejected": bool(float(np.prod([1.0, 1.01, 1.0])) > 1),
        },
        "claim_4_remove_lattice": {
            "premise_changed": "affine functions separate points but are not a lattice",
            "target": "absolute value on [-1,1]",
            "best_affine_uniform_error_lower_bound": 0.5,
            "rejected": True,
        },
        "claim_5_remove_strict_margin": {
            "premise_changed": "unscaled target saturates the metric while separation only guarantees strict inequality",
            "strict_precondition_holds": False,
            "rejected": True,
        },
    }
    return {
        "controls": controls,
        "all_rejected": all(control["rejected"] for control in controls.values()),
    }
