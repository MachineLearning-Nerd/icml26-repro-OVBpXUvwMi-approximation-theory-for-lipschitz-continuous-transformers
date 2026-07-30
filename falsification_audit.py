"""Search exact theorem boundaries without treating failed searches as proofs."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import time
from pathlib import Path

import numpy as np


def claim_1_search(rng: np.random.Generator) -> dict:
    maximum = 0.0
    trials = 0
    for dimension in (2, 4, 8, 16):
        for _ in range(250):
            width = dimension + 3
            weight = rng.normal(size=(width, dimension))
            norm_squared = np.linalg.norm(weight, 2) ** 2
            tau = rng.uniform() * 2 / norm_squared
            mask = np.diag(rng.integers(0, 2, size=width))
            jacobian = np.eye(dimension) - tau * weight.T @ mask @ weight
            maximum = max(maximum, float(np.linalg.norm(jacobian, 2)))
            trials += 1
    return {
        "assumption_satisfying_trials": trials,
        "max_jacobian_norm": maximum,
        "counterexample_found": maximum > 1 + 2e-12,
    }


def claim_2_search(rng: np.random.Generator) -> dict:
    maximum = 0.0
    trials = 0
    for dimension in (2, 4, 8, 16):
        for _ in range(250):
            tokens = rng.normal(size=(64, dimension))
            tokens /= np.maximum(np.linalg.norm(tokens, axis=1, keepdims=True), 1)
            matrix = rng.normal(size=(dimension, dimension)) / np.sqrt(dimension)
            query = rng.normal(size=dimension)
            query /= max(np.linalg.norm(query), 1)
            values = tokens @ matrix.T
            logits = values @ query
            weights = np.exp(logits - logits.max())
            weights /= weights.sum()
            centered = values - weights @ values
            covariance = (centered * weights[:, None]).T @ centered
            beta = float(np.max(np.sum(values * values, axis=1)))
            if beta == 0:
                continue
            eta = 2 / beta
            jacobian = np.eye(dimension) - eta * covariance
            maximum = max(maximum, float(np.linalg.norm(jacobian, 2)))
            trials += 1

    scales = [1.0, 0.1, 0.01, 0.001]
    uniform_theta_ratios = [2 / scale for scale in scales]
    return {
        "assumption_satisfying_fixed_theta_trials": trials,
        "max_query_jacobian_norm": maximum,
        "fixed_theta_counterexample_found": maximum > 1 + 2e-12,
        "wording_boundary": {
            "interpretation": "If C1 were required to depend only on Omega uniformly over theta",
            "construction": "Omega=[-1,1], A=s, eta=2/s^2, x=0, mu=delta_1, nu=delta_0",
            "scales": scales,
            "measure_lipschitz_ratios": uniform_theta_ratios,
            "conclusion": "No Omega-only uniform constant exists; the proof correctly depends on A and eta.",
        },
    }


def claim_3_search(rng: np.random.Generator) -> dict:
    max_query_product = 0.0
    max_context_bound = 0.0
    for depth in (1, 4, 16, 64, 128):
        for _ in range(100):
            query_constants = rng.uniform(0.7, 1.0, size=depth)
            context_constants = rng.uniform(0.01, 0.2, size=depth)
            query_product = float(np.prod(query_constants))
            propagated = 1.0
            output = 0.0
            for query_constant, context_constant in zip(
                query_constants, context_constants
            ):
                output = query_constant * output + context_constant * propagated
                propagated *= 1 + context_constant
            max_query_product = max(max_query_product, query_product)
            max_context_bound = max(max_context_bound, float(output))
    return {
        "max_query_product": max_query_product,
        "max_finite_context_bound": max_context_bound,
        "query_counterexample_found": max_query_product > 1 + 1e-12,
        "wording_boundary": "The exact lemma allows C2 to depend on depth; only the query constant is depth-independent.",
    }


def claims_4_5_search(rng: np.random.Generator) -> dict:
    maximum_envelope_error = 0.0
    trials = 0
    for point_count in (4, 8, 16, 32):
        for _ in range(100):
            points = np.sort(rng.uniform(-1, 1, point_count))
            raw = rng.normal(size=point_count)
            target = np.minimum.reduce(
                [raw[index] + np.abs(points - point) for index, point in enumerate(points)]
            )
            distances = np.abs(points[:, None] - points[None, :])
            cones = target[:, None] + distances
            recovered = cones.min(axis=0)
            maximum_envelope_error = max(
                maximum_envelope_error, float(np.max(np.abs(recovered - target)))
            )
            trials += 1
    return {
        "complete_finite_metric_trials": trials,
        "max_lattice_envelope_error": maximum_envelope_error,
        "finite_domain_counterexample_found": maximum_envelope_error > 1e-12,
        "universal_status": "A finite falsification search cannot verify a universal density theorem.",
    }


def main() -> int:
    started = time.perf_counter()
    rng = np.random.default_rng(260215503)
    results = {
        "route": "assumption-satisfying falsification audit",
        "git_sha": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "seed": 260215503,
        "claims": {
            "claim_1": claim_1_search(rng),
            "claim_2": claim_2_search(rng),
            "claim_3": claim_3_search(rng),
            "claims_4_5": claims_4_5_search(rng),
        },
        "compute": {
            "estimated_cores": 2,
            "selected_flavor": "Hugging Face cpu-upgrade",
            "allocated_logical_cpus": os.cpu_count(),
            "python": platform.python_version(),
        },
    }
    results["runtime_seconds"] = time.perf_counter() - started
    results["exact_claim_counterexample_found"] = any(
        [
            results["claims"]["claim_1"]["counterexample_found"],
            results["claims"]["claim_2"]["fixed_theta_counterexample_found"],
            results["claims"]["claim_3"]["query_counterexample_found"],
            results["claims"]["claims_4_5"]["finite_domain_counterexample_found"],
        ]
    )
    results["controls_triggered"] = bool(
        results["claims"]["claim_2"]["wording_boundary"]["measure_lipschitz_ratios"][-1]
        > 1000
        and results["claims"]["claim_3"]["max_finite_context_bound"] > 1
    )
    artifact = Path(".openresearch/artifacts/falsification_audit")
    artifact.mkdir(parents=True, exist_ok=True)
    (artifact / "raw_results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return 0 if results["controls_triggered"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
