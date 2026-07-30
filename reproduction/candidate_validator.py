"""Validate the evaluator-visible candidate without network or repository context."""

from __future__ import annotations

import json
from pathlib import Path


def _page_files(node: dict) -> list[str]:
    files = [node["file"]]
    for child in node.get("children", []):
        files.extend(_page_files(child))
    return files


def validate_candidate() -> dict:
    candidate = Path("space_candidate")
    logbook = json.loads((candidate / "logbook.json").read_text())
    manifest_lines = Path(
        ".openresearch/protected/judged-space-manifest.sha256"
    ).read_text().splitlines()
    historical = {line.split("  ", 1)[1] for line in manifest_lines}
    referenced = _page_files(logbook["root"])
    missing_pages = [
        path
        for path in referenced
        if not (candidate / path).is_file() and path not in historical
    ]

    claim_errors = []
    for claim_id in range(1, 6):
        text = (
            candidate / f"pages/claim-{claim_id}-current/page.md"
        ).read_text()
        for marker in (
            "**Verdict: VERIFIED.",
            "## Exact contract",
            "## Evidence",
            "[Contract]",
            "[raw result]",
            "[verifier]",
            "Negative control",
        ):
            if marker.lower() not in text.lower():
                claim_errors.append(f"claim {claim_id}: missing {marker}")

    children = logbook["root"]["children"]
    current_first = bool(children and children[0]["slug"] == "current-verification")
    readme_current = "[Current verification](#/current-verification)" in (
        candidate / "README.md"
    ).read_text()

    return {
        "schema_version": logbook.get("schema_version"),
        "space_id": logbook.get("space_id"),
        "referenced_pages": len(referenced),
        "missing_pages": missing_pages,
        "historical_manifest_files": len(historical),
        "claim_page_errors": claim_errors,
        "current_verification_first": current_first,
        "readme_links_current_verification": readme_current,
        "passed": (
            logbook.get("schema_version") == 1
            and logbook.get("space_id") == "DineshAI/OVBpXUvwMi"
            and not missing_pages
            and len(historical) == 17
            and not claim_errors
            and current_first
            and readme_current
        ),
    }
