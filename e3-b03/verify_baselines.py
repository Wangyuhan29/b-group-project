#!/usr/bin/env python3
"""Run E3 B03 reference samples in fresh temporary copies and retain evidence."""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "evidence" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
OUT.mkdir(parents=True, exist_ok=False)


def run(args: list[str], cwd: Path, name: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    (OUT / f"{name}.log").write_text(
        f"cwd={cwd}\ncommand={args!r}\nexit_code={result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n",
        encoding="utf-8",
    )
    if result.returncode != expected:
        raise AssertionError(f"{name}: expected exit {expected}, got {result.returncode}")
    return result


def update_header(path: Path, value: int) -> None:
    time.sleep(1.1)
    path.write_text(f"#define VALUE {value}\n", encoding="utf-8")


def verify_style(style: str, tmp: Path) -> dict[str, object]:
    src = ROOT / "fixtures" / "mdfixer"
    work = tmp / style
    work.mkdir()
    for filename in ("main.c", "config.h"):
        shutil.copy2(src / filename, work / filename)
    shutil.copy2(src / f"{style}.before.mk", work / "Makefile")
    run(["make", "clean"], work, f"{style}-clean-before")
    run(["make"], work, f"{style}-build-before")
    baseline = run(["./app"], work, f"{style}-output-before").stdout.strip()
    assert baseline == "1"
    update_header(work / "config.h", 2)
    run(["make"], work, f"{style}-incremental-before")
    stale = run(["./app"], work, f"{style}-stale-output").stdout.strip()
    assert stale == "1", f"{style}: missing dependency did not produce stale output"

    patch_file = src / f"{style}.patch"
    run(["git", "apply", "--check", str(patch_file)], work, f"{style}-patch-check")
    run(["git", "apply", str(patch_file)], work, f"{style}-patch-apply")
    assert (work / "Makefile").read_bytes() == (src / f"{style}.after.mk").read_bytes()
    run(["make", "clean"], work, f"{style}-clean-after")
    run(["make"], work, f"{style}-build-after")
    clean_output = run(["./app"], work, f"{style}-clean-output").stdout.strip()
    assert clean_output == "2"
    update_header(work / "config.h", 3)
    run(["make"], work, f"{style}-incremental-after")
    repaired = run(["./app"], work, f"{style}-repaired-output").stdout.strip()
    assert repaired == "3"
    if style == "implicit":
        depfile = (work / "main.d").read_text(encoding="utf-8")
        assert "config.h" in depfile
    return {"style": style, "before_incremental": stale, "after_clean": clean_output,
            "after_incremental": repaired, "result": "PASS"}


def verify_rejection(tmp: Path) -> dict[str, object]:
    src = ROOT / "fixtures" / "mdfixer"
    work = tmp / "rejected"
    work.mkdir()
    for filename in ("main.c", "config.h"):
        shutil.copy2(src / filename, work / filename)
    original = (src / "target.before.mk").read_text(encoding="utf-8")
    (work / "Makefile").write_text(original, encoding="utf-8")
    run(["make"], work, "rejection-original-build")
    invalid = original.replace("$(CC) $(CFLAGS) -c main.c -o main.o", "false")
    (work / "Makefile").write_text(invalid, encoding="utf-8")
    run(["make", "clean"], work, "rejection-clean")
    failed = run(["make"], work, "rejection-invalid-build", expected=2)
    assert failed.returncode != 0
    (work / "Makefile").write_text(original, encoding="utf-8")
    run(["make"], work, "rejection-restored-build")
    assert run(["./app"], work, "rejection-restored-output").stdout.strip() == "1"
    return {"invalid_candidate_exit_code": failed.returncode, "restored_output": "1",
            "result": "PASS"}


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="b03-e3-") as dirname:
        tmp = Path(dirname)
        draft = tmp / "draft"
        shutil.copytree(ROOT / "fixtures" / "draft", draft)
        unavailable = subprocess.run(["/bin/sh", "-c", "make"], cwd=draft, text=True,
                                     capture_output=True, env={"PATH": "/nonexistent"}, check=False)
        (OUT / "draft-missing-toolchain-local.log").write_text(
            "provenance=LOCAL_FAILURE_SIMULATION; not a Docker build\n"
            "command=/bin/sh -c make (PATH=/nonexistent)\n"
            f"exit_code={unavailable.returncode}\n"
            f"stdout:\n{unavailable.stdout}\nstderr:\n{unavailable.stderr}\n",
            encoding="utf-8",
        )
        assert unavailable.returncode != 0
        run(["make"], draft, "draft-local-build")
        assert (draft / "hello").is_file()
        assert run(["./hello"], draft, "draft-local-output").stdout == "hello E3\n"
        styles = [verify_style(style, tmp) for style in ("target", "macro", "hybrid", "implicit")]
        rejection = verify_rejection(tmp)
    report = {"provenance": "LOCAL_EXECUTION", "platform": platform.platform(),
              "python": sys.version.split()[0], "draft": "PASS", "styles": styles,
              "invalid_candidate": rejection,
              "draft_failure": {"mode": "LOCAL_MISSING_TOOL_SIMULATION",
                                "exit_code": unavailable.returncode},
              "docker": "NOT_RUN_BY_THIS_SCRIPT", "evidence_directory": str(OUT)}
    (OUT / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
