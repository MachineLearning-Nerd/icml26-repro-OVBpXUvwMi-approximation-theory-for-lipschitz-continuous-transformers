"""Validate the evaluator-visible candidate without network access."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


LIVE_CLAIM_HASHES = {
    1: "9bc1e95974ecebfa399fccfae81ec2d2615f8c4ed08f4d99fdb204695e1918ef",
    2: "3a9f804409b633536ef38ee6b553ce9af3af253ef508b09fb55e444a35f53632",
    3: "9bcae7d8ac5321ee729bb9fd7fa7e522e1338b1efb92c31e6ca24bfc405329d3",
}


def _page_files(node: dict) -> list[str]:
    files = [node["file"]]
    for child in node.get("children", []):
        files.extend(_page_files(child))
    return files


def validate_candidate() -> dict:
    candidate = Path("space_candidate")
    logbook = json.loads((candidate / "logbook.json").read_text())
    children = logbook["root"]["children"]
    slugs = [child["slug"] for child in children]
    expected_slugs = [
        "executive-summary",
        "claim-1-current",
        "claim-2-current",
        "claim-3-current",
        "claim-4-current",
        "claim-5-current",
        "conclusion",
    ]
    referenced = _page_files(logbook["root"])
    missing_pages = [
        path for path in referenced if not (candidate / path).is_file()
    ]

    index = (candidate / "pages/index.md").read_text()
    index_intro = index.split("## Pages", 1)[0].split("\n", 1)[1].strip()
    index_routes = re.findall(r"\(#/([A-Za-z0-9._-]+)\)", index)

    executive = (candidate / "pages/executive-summary/page.md").read_text()
    executive_checks = {
        "pinned_summary": (
            '"title":"Executive summary"' in executive
            and '"pinned":true' in executive
        ),
        "pinned_poster": (
            '"title":"Reproduction poster"' in executive
            and '"poster":true' in executive
        ),
        "poster_embed": "poster_embed.html" in executive,
        "scope_cost_table": "| Scope | Result | Cost / provenance |" in executive,
    }

    claim_errors = []
    for claim_id in range(1, 6):
        path = candidate / f"pages/claim-{claim_id}-current/page.md"
        text = path.read_text()
        for marker in (
            "**Verdict: VERIFIED.",
            "## Exact contract",
            "## Raw evidence" if claim_id >= 4 else "## Evidence",
            "verifier",
            "negative",
            "Fixed command",
            "Limitation",
        ):
            if marker.lower() not in text.lower():
                claim_errors.append(f"claim {claim_id}: missing {marker}")

    preserved_claim_hashes = {
        claim_id: hashlib.sha256(
            (
                candidate
                / f"pages/claim-{claim_id}-current/page.md"
            ).read_bytes()
        ).hexdigest()
        for claim_id in LIVE_CLAIM_HASHES
    }
    claims_1_3_unchanged = preserved_claim_hashes == LIVE_CLAIM_HASHES

    formal_paths = [
        "LipschitzTransformerFormal/RestrictedStoneWeierstrass.lean",
        "LipschitzTransformerFormal/TransformerUniversalApproximation.lean",
        "formal_negative_controls/StrictMarginFails.lean",
        "formal_negative_controls/NegativeCoefficientFails.lean",
        "reproduction/formal_verifier.py",
        ".openresearch/artifacts/claim_4/formal_verification_output.json",
        ".openresearch/artifacts/claim_5/formal_verification_output.json",
    ]
    missing_formal = [path for path in formal_paths if not Path(path).is_file()]

    allowlist_lines = [
        line
        for line in Path("release/upload_allowlist.tsv").read_text().splitlines()
        if line and not line.startswith("#")
    ]
    allowlist_destinations = [line.split("\t", 1)[0] for line in allowlist_lines]
    allowlist_unique = len(allowlist_destinations) == len(
        set(allowlist_destinations)
    )

    result = {
        "schema_version": logbook.get("schema_version"),
        "space_id": logbook.get("space_id"),
        "tags": logbook.get("tags"),
        "page_order": slugs,
        "expected_page_order": expected_slugs,
        "referenced_pages": len(referenced),
        "missing_pages": missing_pages,
        "index_title_pages_only": not index_intro,
        "index_routes": index_routes,
        "executive_checks": executive_checks,
        "claim_page_errors": claim_errors,
        "claims_1_3_live_hashes": preserved_claim_hashes,
        "claims_1_3_unchanged": claims_1_3_unchanged,
        "missing_formal_files": missing_formal,
        "poster_present": (candidate / "poster_embed.html").is_file(),
        "allowlisted_text_files": len(allowlist_destinations),
        "allowlist_unique": allowlist_unique,
        "generated_manifest_listed": (
            "evidence/current/upload-manifest.sha256"
            in allowlist_destinations
        ),
    }
    result["passed"] = (
        result["schema_version"] == 1
        and result["space_id"] == "DineshAI/OVBpXUvwMi"
        and "icml2026-repro" in result["tags"]
        and "paper-OVBpXUvwMi" in result["tags"]
        and slugs == expected_slugs
        and index_routes == expected_slugs
        and not missing_pages
        and result["index_title_pages_only"]
        and all(executive_checks.values())
        and not claim_errors
        and claims_1_3_unchanged
        and not missing_formal
        and result["poster_present"]
        and allowlist_unique
        and result["generated_manifest_listed"]
    )
    return result
