"""Evaluator-only traversal of an assembled Space candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote


ROUTE = re.compile(r"\]\(#/([^)]+)\)")
BLOB = re.compile(
    r"https://huggingface\.co/spaces/DineshAI/OVBpXUvwMi/blob/main/([^)]+)"
)


def flatten(node: dict) -> dict[str, str]:
    result = {node["slug"]: node["file"]}
    for child in node.get("children", []):
        result.update(flatten(child))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate")
    args = parser.parse_args()
    root = Path(args.candidate).resolve()
    opened = []
    missing = []
    conclusions_not_verified = []

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
    texts.extend((root / path).read_text() for path in opened if path.endswith(".md"))
    linked_raw = set()
    for text in texts:
        for slug in ROUTE.findall(text):
            if slug not in routes:
                missing.append(f"route:{slug}")
        for remote_path in BLOB.findall(text):
            relative = unquote(remote_path)
            linked_raw.add(relative)
            if not (root / relative).is_file():
                missing.append(relative)

    claim_checks = {}
    markers = (
        "Verdict:",
        "Confidence:",
        "Exact contract",
        "Evidence",
        "Negative control",
        "Fixed command",
        "Limitation",
    )
    for claim_id in range(1, 6):
        relative = f"pages/claim-{claim_id}-current/page.md"
        text = (root / relative).read_text()
        absent = [marker for marker in markers if marker.lower() not in text.lower()]
        claim_checks[str(claim_id)] = {
            "page": relative,
            "missing_markers": absent,
            "passed": not absent,
        }
        if absent:
            conclusions_not_verified.append(
                f"claim {claim_id} missing {', '.join(absent)}"
            )

    judged_manifest = read("evidence/current/judged-space-manifest.sha256")
    judged_files = {
        line.split("  ", 1)[1] for line in judged_manifest.splitlines() if line
    }
    absent_historical = sorted(path for path in judged_files if not (root / path).is_file())
    if absent_historical:
        missing.extend(absent_historical)

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
        "claim_checks": claim_checks,
        "historical_files_expected": len(judged_files),
        "historical_files_missing": absent_historical,
        "missing": sorted(set(missing)),
        "secret_hits": secret_hits,
        "conclusions_not_verified": conclusions_not_verified,
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
        and not secret_hits
        and not conclusions_not_verified
        and len(judged_files) == 17
    )
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
