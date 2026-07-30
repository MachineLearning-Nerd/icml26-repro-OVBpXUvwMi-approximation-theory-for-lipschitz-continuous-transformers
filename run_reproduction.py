"""Fixed experiment entrypoint for every OpenResearch node."""

import os

for thread_env in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ[thread_env] = "1"

import json
import math
import platform
import time
from pathlib import Path

import numpy as np

import falsification_audit


SEEDS = [0, 1, 2, 3, 5, 7, 11]


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(x, 0.0)


def mlp(x: np.ndarray, weight: np.ndarray, bias: np.ndarray, tau: float) -> np.ndarray:
    return x - tau * weight.T @ relu(weight @ x + bias)


def attention(
    x: np.ndarray, matrix: np.ndarray, tokens: np.ndarray, eta: float
) -> np.ndarray:
    values = tokens @ matrix.T
    logits = values @ x
    weights = np.exp(logits - logits.max())
    weights /= weights.sum()
    return x - eta * weights @ values


def max_pair_ratio(fn, pairs: np.ndarray) -> float:
    ratios = []
    for first, second in pairs:
        denominator = np.linalg.norm(first - second)
        if denominator > 0:
            ratios.append(np.linalg.norm(fn(first) - fn(second)) / denominator)
    return float(max(ratios))


def run_baseline() -> dict:
    started = time.perf_counter()
    rng = np.random.default_rng(0)

    x = rng.uniform(-1, 1, 1)
    weight = rng.normal(size=(3, 1))
    bias = rng.normal(size=3)
    tau = 0.3
    mlp_euler_error = float(
        np.linalg.norm(
            mlp(x, weight, bias, tau)
            - (x - tau * weight.T @ relu(weight @ x + bias))
        )
    )

    tokens = rng.uniform(-1, 1, (15, 1))
    matrix = np.array([[0.5]])
    eta = 0.4
    values = tokens @ matrix.T
    logits = values @ x
    softmax = np.exp(logits - logits.max())
    softmax /= softmax.sum()
    attention_euler_error = float(
        np.linalg.norm(
            attention(x, matrix, tokens, eta)
            - (x - eta * softmax @ values)
        )
    )

    context = np.random.default_rng(1).uniform(-1, 1, (30, 1))
    query_pairs = np.random.default_rng(100).uniform(-1, 1, (300, 2, 1))
    query_ratios = {}
    for candidate_eta in (0.2, 0.5, 0.9):
        query_ratios[str(candidate_eta)] = max_pair_ratio(
            lambda query: attention(query, matrix, context, candidate_eta),
            query_pairs,
        )

    layers = [
        ("attention", np.array([[0.4]]), None, 0.4),
        ("mlp", np.array([[0.5]]), np.array([0.1]), 0.5),
        ("attention", np.array([[-0.3]]), None, 0.4),
        ("mlp", np.array([[0.5]]), np.array([0.1]), 0.5),
    ]

    def deep(query: np.ndarray) -> np.ndarray:
        result = query
        for layer_type, matrix_or_weight, layer_bias, step in layers:
            if layer_type == "attention":
                result = attention(result, matrix_or_weight, context, step)
            else:
                result = mlp(result, matrix_or_weight, layer_bias, step)
        return result

    deep_ratio = max_pair_ratio(deep, query_pairs)

    sample_u = np.random.default_rng(11).uniform(-1, 1, 200)
    sample_x = np.random.default_rng(12).uniform(-1, 1, 200)
    target = np.sin(sample_u) * np.maximum(sample_x, 0)
    tautological_basis = np.column_stack(
        [
            np.ones_like(sample_u),
            np.sin(sample_u) * np.maximum(sample_x, 0),
        ]
    )
    coefficients, *_ = np.linalg.lstsq(tautological_basis, target, rcond=None)
    circular_fit_error = float(
        np.max(np.abs(tautological_basis @ coefficients - target))
    )

    checks = {
        "claim_1_euler_identity": mlp_euler_error == 0 and attention_euler_error == 0,
        "claim_2_sampled_query_ratios": all(
            ratio <= 1 + 1e-12 for ratio in query_ratios.values()
        ),
        "claim_3_four_layer_sampled_ratio": deep_ratio <= 1 + 1e-12,
        "claim_4_circular_target_fit": circular_fit_error <= 1e-12,
        "claim_5_circular_basis_fit": circular_fit_error <= 1e-12,
    }
    runtime = time.perf_counter() - started
    cpu_affinity = None
    if hasattr(os, "sched_getaffinity"):
        cpu_affinity = len(os.sched_getaffinity(0))

    return {
        "artifact_status": "Historical rejected baseline",
        "scientific_scope": "toy",
        "paper": "arXiv:2602.15503",
        "judged_space_revision": "df0a8cc0348a130d23bce8f00c22eaa00452aa3d",
        "seeds": SEEDS,
        "compute": {
            "estimated_cores": 1,
            "selected_flavor": "local CPU",
            "allocated_logical_cpus": os.cpu_count(),
            "affinity_cpus": cpu_affinity,
            "python": platform.python_version(),
            "runtime_seconds": runtime,
        },
        "results": {
            "dimension": 1,
            "max_tokens": 30,
            "layers": 4,
            "mlp_euler_error": mlp_euler_error,
            "attention_euler_error": attention_euler_error,
            "sampled_query_ratios": query_ratios,
            "sampled_deep_ratio": deep_ratio,
            "circular_fit_error": circular_fit_error,
        },
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "limitations": [
            "Finite d=1 samples cannot verify universally quantified Lipschitz claims.",
            "The approximation target is itself a basis column, so the fit is circular.",
            "This run preserves the judged 5/10 baseline and is not current verification.",
        ],
    }


def main() -> int:
    result = run_baseline()
    artifact_dir = Path(".openresearch/artifacts/baseline")
    print(json.dumps({"baseline_regression": result}, indent=2))
    if not result["all_checks_passed"]:
        return 1
    if not math.isfinite(result["compute"]["runtime_seconds"]):
        return 1
    return falsification_audit.main()


if __name__ == "__main__":
    raise SystemExit(main())
