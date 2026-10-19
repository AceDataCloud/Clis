"""Build the service-name directory bundled with the ADC package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(data: dict) -> list[str]:
    errors = []
    seen = set()
    for entry in data["services"]:
        slug = entry["slug"]
        if slug in seen or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            errors.append(f"duplicate or invalid service slug: {slug}")
        seen.add(slug)
        if not entry["search_terms"] or "Ace Data Cloud" not in entry["brand"]:
            errors.append(f"missing service identity/search terms: {slug}")
        if entry["cli_published"] and not entry["cli_repo"]:
            errors.append(f"published CLI has no verified repository: {slug}")
        for field in ("cli_repo", "mcp_repo"):
            value = entry[field]
            if value and not value.startswith("https://github.com/AceDataCloud/"):
                errors.append(f"unexpected publisher in {field}: {slug}")
        if entry["cli_published"] and entry["cli_directory"] == "happyhorse":
            receipt = entry.get("publication_receipt", {})
            version = receipt.get("version", "")
            artifacts = receipt.get("artifacts", [])
            if (
                not re.fullmatch(r"[0-9]+(?:\.[0-9]+)+", version)
                or receipt.get("official_metadata_url")
                != f"https://pypi.org/pypi/{entry['cli_package']}/{version}/json"
                or not receipt.get("workflow_url", "").startswith(
                    "https://github.com/AceDataCloud/HappyHorseCli/actions/runs/"
                )
                or not re.fullmatch(r"[0-9a-f]{40}", receipt.get("source_sha", ""))
                or receipt.get("clean_install_verified") is not True
                or receipt.get("readme_matches_source") is not True
                or len(artifacts) != 2
                or not all(
                    re.fullmatch(r"[0-9a-f]{64}", artifact.get("sha256", ""))
                    for artifact in artifacts
                )
                or not any(
                    artifact.get("filename", "").endswith(".whl")
                    for artifact in artifacts
                )
                or not any(
                    artifact.get("filename", "").endswith(".tar.gz")
                    for artifact in artifacts
                )
            ):
                errors.append(
                    "HappyHorse CLI needs its official version/hash/source/install receipt"
                )
        if entry.get("mcp_command") != "uvx" or not entry.get("mcp_arguments"):
            errors.append(f"missing the exact isolated MCP launch path: {slug}")
        if slug == "gpt-image":
            args = entry.get("mcp_arguments", [])
            if args[-2:] != ["--profile", "gpt-image"] or not any(
                value.startswith("mcp-openai-pro>=") for value in args
            ):
                errors.append(
                    "GPT Image must retain its service profile and minimum package version"
                )
        if not entry["task_commands"]:
            errors.append(f"missing same-task query path: {slug}")
    return errors


def bundled(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write", action="store_true", help="Refresh the ADC package copy"
    )
    args = parser.parse_args()
    data = json.loads((ROOT / "service-packages.json").read_text())
    errors = validate(data)
    target = ROOT / "adc/adc_cli/service_packages.json"
    expected = bundled(data)
    if args.write and not errors:
        target.write_text(expected)
    elif not target.is_file() or target.read_text() != expected:
        errors.append(
            "ADC service directory is stale; run python3 scripts/service_packages.py --write"
        )
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        f"Service directory: {len(data['services'])} entries; published/source-only states preserved"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
