#!/usr/bin/env python3
"""Require README CLI inventory to match sync.yaml mappings."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- canonical-acquisition -->"


def acquisition_url(campaign: str) -> str:
    if not re.fullmatch(r"cli-[a-z0-9-]+", campaign):
        raise ValueError(f"invalid CLI campaign {campaign!r}")
    return (
        "https://platform.acedata.cloud/"
        f"?utm_source=github&utm_medium=repo&utm_campaign={campaign}"
    )


def validate_acquisition(path: Path, campaign: str, errors: list[str]) -> None:
    text = path.read_text()
    url = acquisition_url(campaign)
    expected = f"{MARKER}\n[Get an API token]({url})"
    if text.count(MARKER) != 1:
        errors.append(f"{path.relative_to(ROOT)}: expected one acquisition marker")
    if text.count(url) != 1 or expected not in text:
        errors.append(f"{path.relative_to(ROOT)}: missing canonical {campaign} link")


def main() -> int:
    mappings = set(re.findall(r"^  ([a-z0-9_-]+):\s*$", (ROOT / "sync.yaml").read_text(), re.MULTILINE))
    listed = set(re.findall(r"^\| `([^/`]+)/`", (ROOT / "README.md").read_text(), re.MULTILINE))
    missing = sorted(mappings - listed)
    extra = sorted(listed - mappings)
    errors: list[str] = []
    if missing:
        errors.append(f"README missing mapped CLIs: {', '.join(missing)}")
    if extra:
        errors.append(f"README lists unmapped CLIs: {', '.join(extra)}")
    validate_acquisition(ROOT / "README.md", "cli-catalog", errors)
    for alias in sorted(mappings):
        validate_acquisition(ROOT / alias / "README.md", f"cli-{alias}", errors)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"README inventory and acquisition links match {len(mappings)} mapped CLIs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
