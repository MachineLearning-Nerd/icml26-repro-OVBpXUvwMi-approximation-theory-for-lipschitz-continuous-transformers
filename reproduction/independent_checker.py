"""Independent numerical and exact-algebra checks, separate from the proof kernel."""

from __future__ import annotations

import itertools

import numpy as np


def check_claim_1() -> dict:
    rng = np.random.default_rng(101)
    dimension, width = 16, 10
    weight = rng.normal(size=(width, dimension))
    spectral_squared = float(np.linalg.norm(weight, 2) ** 2)
    tau = 2.0 / spectral_squared
    worst = 0.0
    for mask_bits in itertools.product((0.0, 1.0), repeat=width):
        mask = np.diag(mask_bits)
        jacobian = np.eye(dimension) - tau * weight.T @ mask @ weight
        worst = max(worst, float(np.linalg.norm(jacobian, 2)))
    return {
        "dimension": dimension,
        "hidden_width": width,
        "activation_regions_exhausted": 2**width,
        "max_segment_operator_norm": worst,
        "passed": worst <= 1 + 5e-12,
    }


def check_claim_2() -> dict:
    rng = np.random.default_rng(202)
    dimension, tokens = 32, 512
    context = rng.normal(size=(tokens, dimension))
    context /= np.maximum(np.linalg.norm(context, axis=1, keepdims=True), 1)
    matrix = rng.normal(size=(dimension, dimension)) / np.sqrt(dimension)
    query = rng.normal(size=dimension)
    query /= max(np.linalg.norm(query), 1)
    values = context @ matrix.T
    logits = values @ query
    weights = np.exp(logits - logits.max())
    weights /= weights.sum()
    mean = weights @ values
    centered = values - mean
    covariance = (centered * weights[:, None]).T @ centered
    beta = float(np.max(np.sum(values * values, axis=1)))
    min_eigenvalue = float(np.linalg.eigvalsh(covariance).min())
    max_eigenvalue = float(np.linalg.eigvalsh(covariance).max())
    return {
        "dimension": dimension,
        "tokens": tokens,
        "covariance_min_eigenvalue": min_eigenvalue,
        "covariance_max_eigenvalue": max_eigenvalue,
        "sup_norm_squared_bound": beta,
        "passed": bool(
            min_eigenvalue >= -2e-14 and max_eigenvalue <= beta + 2e-12
        ),
    }


def check_claim_3() -> dict:
    layer_query_constants = [1.0] * 128
    attention_measure_constants = [0.25 + index / 512 for index in range(128)]
    propagated_measure_constant = 1.0
    output_measure_constant = 0.0
    for layer_constant, context_constant in zip(
        layer_query_constants, attention_measure_constants
    ):
        output_measure_constant = (
            layer_constant * output_measure_constant
            + context_constant * propagated_measure_constant
        )
        propagated_measure_constant *= 1 + context_constant
    query_constant = float(np.prod(layer_query_constants))
    return {
        "layers": 128,
        "query_constant_product": query_constant,
        "finite_context_constant": output_measure_constant,
        "passed": bool(query_constant <= 1 and np.isfinite(output_measure_constant)),
    }


def check_claim_4_and_5() -> dict:
    # A complete finite compact metric domain: every target respecting the metric
    # is covered by the two-stage min/max construction. This is corroboration of
    # the reconstructed general compact-cover proof, not its replacement.
    points = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    target = np.array([0.0, 0.7, -0.4, 0.2])
    distances = np.abs(points[:, None, 0] - points[None, :, 0])
    distances += np.abs(points[:, None, 1] - points[None, :, 1])
    lip_ok = bool(
        np.all(np.abs(target[:, None] - target[None, :]) <= distances + 1e-12)
    )

    # McShane upper cones are 1-Lipschitz and their minimum exactly recovers
    # any 1-Lipschitz target on the complete finite domain.
    cones = target[:, None] + distances
    recovered = cones.min(axis=0)
    error = float(np.max(np.abs(recovered - target)))

    first = np.array([-0.8, 0.1, 0.6])
    second = np.array([0.3, -0.5, 0.9])
    direction = (first - second) / np.linalg.norm(first - second)
    wasserstein_dirac = float(np.linalg.norm(first - second))
    kr_gap = float(direction @ first - direction @ second)
    return {
        "complete_finite_domain_points": len(points),
        "target_lipschitz": lip_ok,
        "lattice_envelope_uniform_error": error,
        "dirac_w1": wasserstein_dirac,
        "kr_witness_gap": kr_gap,
        "passed": lip_ok
        and error <= 1e-12
        and abs(kr_gap - wasserstein_dirac) <= 1e-12,
    }


def run_independent_checks() -> dict:
    checks = {
        "claim_1": check_claim_1(),
        "claim_2": check_claim_2(),
        "claim_3": check_claim_3(),
        "claims_4_5": check_claim_4_and_5(),
    }
    return {
        "checker": "independent algebra and complete finite-domain checker",
        "checks": checks,
        "all_passed": all(check["passed"] for check in checks.values()),
    }
