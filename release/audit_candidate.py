"""Evaluator-only traversal and protected-tree audit of a Space candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote


ROUTE = re.compile(r"\]\(#/([^)]+)\)")
BLOB = re.compile(
    r"https://huggingface\.co/spaces/DineshAI/OVBpXUvwMi/(?:blob|tree)/main/([^)]+)"
)


def flatten(node: dict) -> dict[str, str]:
    result = {node["slug"]: node["file"]}
    for child in node.get("children", []):
        result.update(flatten(child))
    return result


def load_manifest(path: Path) -> dict[str, str]:
    result = {}
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        digest, relative = line.split("  ", 1)
        result[relative] = digest
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate")
    args = parser.parse_args()
    root = Path(args.candidate).resolve()
    opened = []
    missing = []

    def read(relative: str) -> str:
        path = root / relative
        if not path.is_file():
            missing.append(relative)
            return ""
        opened.append(relative)
        return path.read_text()

    readme = read("README.md")
    logbook_text = read("logbook.json")
    index = read("pages/index.md")
    logbook = json.loads(logbook_text)
    routes = flatten(logbook["root"])
    for relative in dict.fromkeys(routes.values()):
        read(relative)

    texts = [readme, index]
    texts.extend(
        (root / path).read_text()
        for path in opened
        if path.endswith(".md") and (root / path).is_file()
    )
    linked_raw = set()
    for text in texts:
        for slug in ROUTE.findall(text):
            if slug not in routes:
                missing.append(f"route:{slug}")
        for remote_path in BLOB.findall(text):
            relative = unquote(remote_path)
            if relative in {"formal_negative_controls", "pages"}:
                continue
            linked_raw.add(relative)
            if not (root / relative).is_file():
                missing.append(relative)

    marker_errors = []
    for claim_id in range(1, 6):
        relative = f"pages/claim-{claim_id}-current/page.md"
        text = read(relative)
        markers = (
            "Verdict:",
            "Confidence:",
            "Exact contract",
            "Evidence",
            "Negative",
            "Fixed command",
            "Limitation",
        )
        absent = [marker for marker in markers if marker.lower() not in text.lower()]
        if absent:
            marker_errors.append(f"claim {claim_id}: {', '.join(absent)}")

    protected = load_manifest(
        root / "evidence/current/live-8of10-space-manifest.sha256"
    )
    protected_missing = sorted(
        relative for relative in protected if not (root / relative).is_file()
    )
    modified_destinations = {
        line.split("  ", 1)[1]
        for line in (root / "evidence/current/upload-manifest.sha256")
        .read_text()
        .splitlines()
        if line and not line.startswith("#") and "  " in line
    }
    modified_destinations.add("evidence/current/upload-manifest.sha256")
    protected_changed = []
    for relative, expected in protected.items():
        path = root / relative
        if not path.is_file() or relative in modified_destinations:
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            protected_changed.append(relative)

    live_claim_hashes = {
        1: "9bc1e95974ecebfa399fccfae81ec2d2615f8c4ed08f4d99fdb204695e1918ef",
        2: "3a9f804409b633536ef38ee6b553ce9af3af253ef508b09fb55e444a35f53632",
        3: "9bcae7d8ac5321ee729bb9fd7fa7e522e1338b1efb92c31e6ca24bfc405329d3",
    }
    claims_1_3_unchanged = all(
        hashlib.sha256(
            (root / f"pages/claim-{claim_id}-current/page.md").read_bytes()
        ).hexdigest()
        == digest
        for claim_id, digest in live_claim_hashes.items()
    )

    secret_patterns = {
        "private_key": re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
        "hf_token": re.compile(r"hf_[A-Za-z0-9]{20,}"),
        "openai_key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    }
    secret_hits = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for name, pattern in secret_patterns.items():
            if pattern.search(text):
                secret_hits.append(f"{name}:{path.relative_to(root)}")

    result = {
        "audit": "evaluator-blind candidate traversal",
        "entrypoints": ["README.md", "logbook.json", "pages/index.md"],
        "files_opened": list(dict.fromkeys(opened)),
        "linked_raw_files_checked": sorted(linked_raw),
        "marker_errors": marker_errors,
        "protected_revision": "c09976f4189cfa624d6dbb8ac4ef96d14eb113e3",
        "protected_files_expected": len(protected),
        "protected_files_missing": protected_missing,
        "protected_unallowlisted_hash_changes": protected_changed,
        "claims_1_3_unchanged": claims_1_3_unchanged,
        "missing": sorted(set(missing)),
        "secret_hits": secret_hits,
        "tree_sha256": hashlib.sha256(
            "\n".join(
                sorted(
                    str(path.relative_to(root))
                    + ":"
                    + hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in root.rglob("*")
                    if path.is_file()
                )
            ).encode()
        ).hexdigest(),
    }
    result["passed"] = (
        not result["missing"]
        and not marker_errors
        and not protected_missing
        and not protected_changed
        and claims_1_3_unchanged
        and not secret_hits
    )
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
