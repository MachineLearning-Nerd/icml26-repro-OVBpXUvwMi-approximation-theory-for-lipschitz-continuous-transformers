from pathlib import Path

from reproduction.proof_verifier import verify_certificate

raise SystemExit(
    0
    if verify_certificate(Path("reproduction/proof_dag.json"))["claims"]["claim_3"][
        "certificate_passed"
    ]
    else 1
)
