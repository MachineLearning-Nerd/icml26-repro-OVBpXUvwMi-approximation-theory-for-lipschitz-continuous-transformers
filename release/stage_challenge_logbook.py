"""Stage the canonical pages in Trackio's validator layout."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


PAGE_SOURCES = {
    "executive-summary": "pages/executive-summary/page.md",
    "claim-1-current": "pages/claim-1-current/page.md",
    "claim-2-current": "pages/claim-2-current/page.md",
    "claim-3-current": "pages/claim-3-current/page.md",
    "claim-4-current": "pages/claim-4-current/page.md",
    "claim-5-current": "pages/claim-5-current/page.md",
    "conclusion": "pages/conclusion-current/page.md",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    source = repo / "space_candidate"
    output = Path(args.output).resolve()
    trackio = output / ".trackio"
    if trackio.exists():
        raise SystemExit(f"output already exists: {trackio}")

    pages = trackio / "logbook" / "pages"
    pages.mkdir(parents=True)
    shutil.copy2(source / "pages/index.md", pages / "index.md")
    for slug, relative in PAGE_SOURCES.items():
        destination = pages / slug / "page.md"
        destination.parent.mkdir()
        shutil.copy2(source / relative, destination)
    shutil.copy2(source / "poster_embed.html", trackio / "logbook/poster_embed.html")
    (trackio / "metadata.json").write_text(
        json.dumps(
            {
                "space_id": "DineshAI/OVBpXUvwMi",
                "tags": ["icml2026-repro", "paper-OVBpXUvwMi"],
            },
            indent=2,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
