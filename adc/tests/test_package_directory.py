"""Service discovery is offline and separates published and source-only paths."""

import json

from click.testing import CliRunner

from adc_cli.main import cli


def test_service_name_aliases_work_without_a_token(monkeypatch):
    monkeypatch.delenv("ACEDATACLOUD_API_TOKEN", raising=False)
    runner = CliRunner()
    for query, slug in [
        ("Suno", "suno"),
        ("happy horse", "happyhorse"),
        ("gpt image", "gpt-image"),
        ("nano-banana", "nano-banana"),
    ]:
        result = runner.invoke(cli, ["packages", query, "--json"])
        assert result.exit_code == 0
        assert [item["slug"] for item in json.loads(result.output)["services"]] == [slug]


def test_source_only_cli_is_not_an_install_recommendation():
    result = CliRunner().invoke(cli, ["packages", "happyhorse"])
    assert result.exit_code == 0
    assert "source only" in result.output
    assert "pip install happyhorse-cli" not in result.output
    assert "mcp-happyhorse" in result.output


def test_gpt_image_points_at_the_existing_ace_owned_package():
    result = CliRunner().invoke(cli, ["packages", "gpt-image", "--json"])
    entry = json.loads(result.output)["services"][0]
    assert entry["cli_package"] == "openai-pro-cli"
    assert entry["mcp_package"] == "mcp-openai-pro"
    assert "third-party" in entry["note"]


def test_unknown_query_does_not_invent_a_service():
    result = CliRunner().invoke(cli, ["packages", "not-a-service", "--json"])
    assert result.exit_code == 0
    assert json.loads(result.output)["services"] == []
