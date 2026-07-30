"""Assemble a candidate Space from the protected judged tree and text allowlist."""

from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("judged")
    parser.add_argument("output")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    judged = Path(args.judged).resolve()
    output = Path(args.output).resolve()
    if output.exists():
        raise SystemExit(f"output already exists: {output}")
    shutil.copytree(judged, output, ignore=shutil.ignore_patterns(".git"))

    manifest = []
    generated_destination = None
    allowlist = repo / "release/upload_allowlist.tsv"
    for line in allowlist.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        destination, source = line.split("\t")
        if source == "@generated":
            generated_destination = destination
            continue
        source_path = repo / source
        payload = source_path.read_bytes()
        payload.decode("utf-8")
        if b"\0" in payload:
            raise SystemExit(f"binary payload rejected: {source}")
        destination_path = output / destination
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        destination_path.write_bytes(payload)
        manifest.append(
            f"{hashlib.sha256(payload).hexdigest()}  {destination}"
        )

    if generated_destination != "evidence/current/upload-manifest.sha256":
        raise SystemExit("allowlist must contain the generated upload manifest")
    manifest_payload = (
        "# SHA-256 for every uploaded text file except this manifest itself.\n"
        + "\n".join(sorted(manifest))
        + "\n"
    ).encode()
    manifest_path = output / generated_destination
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_bytes(manifest_payload)
    print(f"candidate_files={sum(path.is_file() for path in output.rglob('*'))}")
    print(f"allowlisted_text_files={len(manifest) + 1}")
    print(f"manifest_sha256={hashlib.sha256(manifest_payload).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
