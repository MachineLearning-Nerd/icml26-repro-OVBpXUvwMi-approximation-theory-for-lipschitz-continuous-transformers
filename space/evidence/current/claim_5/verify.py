import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from reproduction.proof_verifier import verify_certificate

formal = json.loads(
    Path(".openresearch/artifacts/claim_5/formal_verification_output.json").read_text()
)
source_hashes = {
    path.name: hashlib.sha256(path.read_bytes()).hexdigest()
    for path in Path("LipschitzTransformerFormal").glob("*.lean")
}
required = {
    "RestrictedStoneWeierstrass.lean",
    "TransformerUniversalApproximation.lean",
}
passed = (
    formal["all_passed"]
    and formal["kernel"]["build_returncode"] == 0
    and formal["kernel"]["no_sorry_axiom"]
    and not formal["kernel"]["forbidden_tokens"]
    and required == set(source_hashes)
    and verify_certificate(Path("reproduction/proof_dag.json"))["claims"]["claim_5"][
        "certificate_passed"
    ]
)
raise SystemExit(0 if passed else 1)
