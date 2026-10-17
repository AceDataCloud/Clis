#!/usr/bin/env python3
"""Require the mirrored CLI inventory and current README attribution contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
# Retain the historical source/mirror mapping without advertising it as active.
RETIRED = {"sora"}
UTM_KEYS = {"utm_source", "utm_medium", "utm_campaign", "utm_content"}
PLATFORM_URL = re.compile(r"https://(?:platform|studio)\.acedata\.cloud[^\s)<\"']*")


def attribution_errors(text: str, entry: str) -> list[str]:
    """Check clickable prose links while preserving API/configuration examples."""
    errors = []
    urls = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker[1][0]
            elif marker[1][0] == fence:
                fence = None
            continue
        if fence is not None:
            continue
        prose = re.sub(r"(`+)(.*?)\1", "", line)
        urls.extend(PLATFORM_URL.findall(prose))
    found_api_key = False
    for url in urls:
        parts = urlsplit(url)
        if parts.path.startswith("/api/"):
            continue
        query = parse_qs(parts.query.replace("&amp;", "&"), keep_blank_values=True)
        expected = {
            "utm_source": "opensource",
            "utm_medium": "referral",
            "utm_campaign": "evergreen",
        }
        if any(query.get(key) != [value] for key, value in expected.items()):
            errors.append(f"expected opensource/referral/evergreen attribution: {url}")
        content = query.get("utm_content", [])
        if len(content) != 1 or not re.fullmatch(r"[a-z0-9][a-z0-9_.-]{0,95}", content[0]):
            errors.append(f"missing or malformed utm_content: {url}")
        elif not content[0].startswith(f"{entry}_readme_"):
            errors.append(f"utm_content belongs to another CLI: {url}")
        if {key for key in query if key.startswith("utm_")} != UTM_KEYS:
            errors.append(f"unexpected or missing UTM fields: {url}")
        if parts.path == "/console/applications" and content == [f"{entry}_readme_api_key"]:
            found_api_key = True
    if not found_api_key:
        errors.append("missing the attributed Applications API key entry")
    return errors


def main() -> int:
    mappings = set(re.findall(r"^  ([a-z0-9_-]+):\s*$", (ROOT / "sync.yaml").read_text(), re.MULTILINE))
    listed = set(re.findall(r"^\| `([^/`]+)/`", (ROOT / "README.md").read_text(), re.MULTILINE))
    missing = sorted(mappings - listed)
    extra = sorted(listed - mappings)
    if missing or extra:
        if missing:
            print(f"README missing mapped CLIs: {', '.join(missing)}", file=sys.stderr)
        if extra:
            print(f"README lists unmapped CLIs: {', '.join(extra)}", file=sys.stderr)
        return 1
    readmes = [(ROOT / "README.md", "cli_catalog")]
    readmes.extend((ROOT / alias / "README.md", alias.replace("-", "_") + "_cli") for alias in sorted(mappings - RETIRED))
    errors = []
    for path, entry in readmes:
        if not path.is_file():
            errors.append(f"{path.relative_to(ROOT)}: missing README")
            continue
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in attribution_errors(path.read_text(), entry))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"README inventory matches {len(mappings)} mappings; attribution passes for catalog + {len(mappings - RETIRED)} active CLIs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
