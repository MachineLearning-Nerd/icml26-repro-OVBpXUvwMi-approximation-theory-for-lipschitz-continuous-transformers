"""Run the pinned Lean kernel checks used for Claims 4 and 5."""

from __future__ import annotations

import hashlib
import os
import platform
import subprocess
import tarfile
import time
import urllib.request
from pathlib import Path


ELAN_URL = (
    "https://github.com/leanprover/elan/releases/download/v4.1.2/"
    "elan-x86_64-unknown-linux-gnu.tar.gz"
)
ELAN_SHA256 = "f81c2e48c1588d4612cd2c8851947898a45ac8d72748a07dff3a5694f1cf589b"
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def run(command: list[str], env: dict[str, str], timeout: int = 1800) -> dict:
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=env,
        timeout=timeout,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "runtime_seconds": time.perf_counter() - started,
    }


def install_elan(cache_dir: Path) -> Path:
    elan_home = cache_dir / "elan"
    elan = elan_home / "bin" / "elan"
    if elan.exists():
        return elan

    cache_dir.mkdir(parents=True, exist_ok=True)
    archive = cache_dir / "elan-v4.1.2.tar.gz"
    request = urllib.request.Request(
        ELAN_URL, headers={"User-Agent": "OpenResearch-Formalization/1.0"}
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        archive.write_bytes(response.read())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != ELAN_SHA256:
        raise RuntimeError(f"elan archive SHA-256 mismatch: {digest}")

    extract_dir = cache_dir / "elan-installer"
    extract_dir.mkdir(exist_ok=True)
    with tarfile.open(archive) as tar:
        tar.extractall(extract_dir, filter="data")
    installer = extract_dir / "elan-init"
    env = os.environ.copy()
    env["ELAN_HOME"] = str(elan_home)
    installed = subprocess.run(
        [
            str(installer),
            "-y",
            "--no-modify-path",
            "--default-toolchain",
            "none",
        ],
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )
    if installed.returncode != 0:
        raise RuntimeError(f"elan installation failed: {installed.stderr}")
    return elan


def verify_formalization(root: Path = Path(".")) -> dict:
    started = time.perf_counter()
    sources = sorted((root / "LipschitzTransformerFormal").glob("**/*.lean"))
    source_text = "\n".join(path.read_text() for path in sources)
    forbidden = [
        token
        for token in ("sorry", "admit", "axiom ")
        if token in source_text
    ]

    cache_dir = root / ".formal-cache"
    elan = install_elan(cache_dir)
    env = os.environ.copy()
    env["ELAN_HOME"] = str(cache_dir / "elan")
    env["PATH"] = f"{elan.parent}:{env.get('PATH', '')}"
    env["LAKE_JOBS"] = "1"

    lake = elan.parent / "lake"
    update = run([str(lake), "update"], env)
    if update["returncode"] != 0:
        return {
            "checker": "Lean 4 kernel",
            "stage": "lake update",
            "forbidden_tokens": forbidden,
            "update": update,
            "all_passed": False,
        }
    cache = run([str(lake), "exe", "cache", "get"], env)
    if cache["returncode"] != 0:
        return {
            "checker": "Lean 4 kernel",
            "stage": "mathlib cache",
            "forbidden_tokens": forbidden,
            "update": update,
            "cache": cache,
            "all_passed": False,
        }
    build = run([str(lake), "build"], env)
    lean_version = run([str(elan.parent / "lean"), "--version"], env, timeout=60)
    negative = run(
        [
            str(lake),
            "env",
            "lean",
            "formal_negative_controls/StrictMarginFails.lean",
        ],
        env,
        timeout=300,
    )

    build_output = build["stdout"] + build["stderr"]
    no_unsafe_axioms = "sorryAx" not in build_output
    negative_rejected = (
        negative["returncode"] != 0
        and "no goals to be solved" not in negative["stderr"]
    )
    passed = (
        not forbidden
        and build["returncode"] == 0
        and no_unsafe_axioms
        and negative_rejected
    )
    return {
        "checker": "Lean 4 kernel",
        "platform": platform.platform(),
        "lean_toolchain": (root / "lean-toolchain").read_text().strip(),
        "mathlib_revision": "v4.19.0",
        "formal_sources": [str(path) for path in sources],
        "forbidden_tokens": forbidden,
        "standard_kernel_axioms_allowed": sorted(STANDARD_AXIOMS),
        "lean_version": lean_version,
        "lake_update": update,
        "mathlib_cache": cache,
        "build": build,
        "negative_control": negative,
        "negative_control_rejected": negative_rejected,
        "no_sorry_axiom": no_unsafe_axioms,
        "runtime_seconds": time.perf_counter() - started,
        "all_passed": passed,
    }
