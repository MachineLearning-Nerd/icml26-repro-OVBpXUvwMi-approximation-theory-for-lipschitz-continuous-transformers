"""Controls that must be rejected for the theorem-specific reason."""

from __future__ import annotations

import numpy as np


def run_negative_controls() -> dict:
    oversized_mlp_jacobian = float(
        np.linalg.norm(np.eye(1) - 2.1 * np.ones((1, 1)), 2)
    )

    values = np.array([[-1.0], [1.0]])
    centered = values - values.mean(axis=0)
    covariance = centered.T @ centered / len(values)
    oversized_attention_jacobian = float(
        np.linalg.norm(np.eye(1) - 2.1 * covariance, 2)
    )

    # If |a x + b - |x|| <= e at x=-1,0,1, averaging the two endpoint
    # constraints and combining with the origin constraint forces e >= 1/2.
    best_affine_uniform_error_lower_bound = 0.5

    saturated_gap = abs(1.0 - 0.0)
    saturated_distance = abs(1.0 - 0.0)

    controls = {
        "claim_1_oversized_step": {
            "premise_changed": "tau=2.1/||W||^2 exceeds the closed admissible interval",
            "observed_lipschitz": oversized_mlp_jacobian,
            "rejected": oversized_mlp_jacobian > 1,
        },
        "claim_2_oversized_attention_step": {
            "premise_changed": "eta=2.1/beta for a two-point context",
            "observed_jacobian_norm_at_origin": oversized_attention_jacobian,
            "rejected": oversized_attention_jacobian > 1,
        },
        "claim_3_expansive_layer": {
            "premise_changed": "one layer has query Lipschitz constant 1.01",
            "observed_composition_bound": 1.01,
            "rejected": bool(float(np.prod([1.0, 1.01, 1.0])) > 1),
        },
        "claim_4_remove_lattice": {
            "premise_changed": "affine functions separate points but are not a lattice",
            "target": "absolute value on [-1,1]",
            "best_affine_uniform_error_lower_bound": best_affine_uniform_error_lower_bound,
            "rejected": best_affine_uniform_error_lower_bound > 0,
        },
        "claim_5_remove_strict_margin": {
            "premise_changed": "unscaled target saturates the metric while separation only guarantees strict inequality",
            "target_gap": saturated_gap,
            "metric_distance": saturated_distance,
            "strict_precondition_holds": saturated_gap < saturated_distance,
            "rejected": not saturated_gap < saturated_distance,
        },
    }
    return {
        "controls": controls,
        "all_rejected": all(control["rejected"] for control in controls.values()),
    }
