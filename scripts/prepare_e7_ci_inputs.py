"""Prepare explicit CI input copies using official registry, preserving digests."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def prepare(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError("Use a fresh CI input directory")
    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(root / "fixtures/draft", output / "fixture")
    changes = []
    for source, target in [(root / "fixtures/draft/Dockerfile.broken", output / "fixture/Dockerfile.broken"),
                           (root / "fixtures/ci-candidates/B03-E5.Dockerfile", output / "candidate.Dockerfile")]:
        original = source.read_text()
        text = original.replace("m.daocloud.io/docker.io/library/", "docker.io/library/")
        text = text.replace("https://mirrors.huaweicloud.com", "https://deb.debian.org")
        if original.splitlines()[0].split("@", 1)[1] != text.splitlines()[0].split("@", 1)[1]:
            raise ValueError("CI adaptation must preserve FROM digest")
        target.write_text(text)
        changes.append({"source": str(source.relative_to(root)), "output": str(target.relative_to(output)),
                        "source_sha256": hashlib.sha256(original.encode()).hexdigest(),
                        "adapted_sha256": hashlib.sha256(text.encode()).hexdigest(),
                        "from_digest": text.splitlines()[0].split("@", 1)[1]})
    report = {"scope": "CI-only copied inputs; use official registry and Debian download source, same pinned digest and build/runtime commands", "files": changes}
    (output / "adaptation.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(Path(__file__).resolve().parents[1], args.out), indent=2))
