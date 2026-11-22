#!/usr/bin/env python3
"""Require the mirrored CLI inventory and current README attribution contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

try:
    from .service_packages import bundled, validate
except ImportError:
    from service_packages import bundled, validate

ROOT = Path(__file__).resolve().parents[1]
# Retain the historical source/mirror mapping without advertising it as active.
RETIRED = {"sora"}
UTM_KEYS = {"utm_source", "utm_medium", "utm_campaign"}
PLATFORM_URL = re.compile(r"https://(?:platform|studio|docs)\.acedata\.cloud[^\s)<\"']*")


def markdown_segments(text: str):
    """Yield (is_prose, text) without changing code fences or inline code."""
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"\s*(`{3,}|~{3,})", line)
        if marker and fence is None:
            fence = marker[1]
            yield False, line
        elif marker and fence and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not line[marker.end():].strip():
            fence = None
            yield False, line
        elif fence:
            yield False, line
        else:
            for index, chunk in enumerate(re.split(r"(`+[^`\n]*`+)", line)):
                yield index % 2 == 0, chunk


def pypi_readme(text: str) -> str:
    """Keep the GitHub text and change tracking only on first-party package links."""
    def replace_source(match: re.Match[str]) -> str:
        url = match[0]
        if urlsplit(url).hostname not in {"platform.acedata.cloud", "studio.acedata.cloud", "docs.acedata.cloud"}:
            return url
        return re.sub(r"([?&](?:amp;)?)utm_source=github(?=&|#|$)", r"\1utm_source=pypi", url)

    return "".join(PLATFORM_URL.sub(replace_source, part) if prose else part for prose, part in markdown_segments(text))


def attribution_errors(text: str, source: str = "github") -> list[str]:
    """Check clickable prose links while preserving API/configuration examples."""
    errors = []
    urls = [url for prose, part in markdown_segments(text) if prose for url in PLATFORM_URL.findall(part)]
    found_api_key = False
    for url in urls:
        parts = urlsplit(url)
        if parts.path.startswith("/api/"):
            continue
        query = parse_qs(parts.query.replace("&amp;", "&"), keep_blank_values=True)
        expected = {
            "utm_source": source,
            "utm_medium": "referral",
            "utm_campaign": "evergreen",
        }
        if any(query.get(key) != [value] for key, value in expected.items()):
            errors.append(f"expected {source}/referral/evergreen attribution: {url}")
        if {key for key in query if key.startswith("utm_")} != UTM_KEYS:
            errors.append(f"unexpected or missing UTM fields: {url}")
        if parts.path == "/console/applications":
            found_api_key = True
    if not found_api_key:
        errors.append("missing the attributed Applications API key entry")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-pypi", action="store_true", help="refresh derived package descriptions")
    args = parser.parse_args()
    mappings = set(
        re.findall(
            r"^  ([a-z0-9_-]+):\s*$", (ROOT / "sync.yaml").read_text(), re.MULTILINE
        )
    )
    listed = set(
        re.findall(r"^\| `([^/`]+)/`", (ROOT / "README.md").read_text(), re.MULTILINE)
    )
    missing = sorted(mappings - listed)
    extra = sorted(listed - mappings)
    if missing or extra:
        if missing:
            print(f"README missing mapped CLIs: {', '.join(missing)}", file=sys.stderr)
        if extra:
            print(f"README lists unmapped CLIs: {', '.join(extra)}", file=sys.stderr)
        return 1
    readmes = [ROOT / "README.md"]
    readmes.extend(
        ROOT / alias / "README.md"
        for alias in sorted(mappings)
    )
    errors = []
    package_data = json.loads((ROOT / "service-packages.json").read_text())
    errors.extend(validate(package_data))
    package_copy = ROOT / "adc/adc_cli/service_packages.json"
    if not package_copy.is_file() or package_copy.read_text() != bundled(package_data):
        errors.append(
            "ADC service directory is stale; run python3 scripts/service_packages.py --write"
        )
    for path in readmes:
        if not path.is_file():
            errors.append(f"{path.relative_to(ROOT)}: missing README")
            continue
        text = path.read_text()
        if path.parent.name not in RETIRED:
            errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in attribution_errors(text))
        if path.parent != ROOT:
            package_path = path.with_name("README.pypi.md")
            expected = pypi_readme(text)
            if args.write_pypi:
                package_path.write_text(expected)
            if not package_path.exists() or package_path.read_text() != expected:
                errors.append(f"{package_path.relative_to(ROOT)} is stale; use --write-pypi")
            elif path.parent.name not in RETIRED:
                errors.extend(f"{package_path.relative_to(ROOT)}: {error}" for error in attribution_errors(expected, "pypi"))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        f"README inventory matches {len(mappings)} mappings; attribution passes for catalog + {len(mappings - RETIRED)} active CLIs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
