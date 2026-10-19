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


def test_source_only_cli_is_not_an_install_recommendation(monkeypatch, tmp_path):
    from importlib import import_module

    directory = import_module("adc_cli.commands.packages")
    data = json.loads(directory.files("adc_cli").joinpath("service_packages.json").read_text())
    entry = next(item for item in data["services"] if item["slug"] == "happyhorse")
    entry["cli_published"] = False
    (tmp_path / "service_packages.json").write_text(json.dumps(data))
    monkeypatch.setattr(directory, "files", lambda _name: tmp_path)
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
    assert entry["mcp_profile"] == "gpt-image"
    assert entry["mcp_min_version"] == "2026.10.18.2"
    assert entry["mcp_arguments"][-2:] == ["--profile", "gpt-image"]
    assert entry["mcp_registry_name"] == "io.github.AceDataCloud/mcp-gpt-image"


def test_unknown_query_does_not_invent_a_service():
    result = CliRunner().invoke(cli, ["packages", "not-a-service", "--json"])
    assert result.exit_code == 0
    assert json.loads(result.output)["services"] == []


def test_gpt_image_text_launch_preserves_five_tool_profile():
    result = CliRunner().invoke(cli, ["packages", "gpt image"])
    assert result.exit_code == 0
    assert "--profile gpt-image" in result.output
    assert "mcp-openai-pro>=2026.10.18.2" in result.output
    assert "five image/task tools" in result.output
    assert "not a separate PyPI package" in result.output


def test_published_happyhorse_offers_a_verified_install_entry():
    runner = CliRunner()
    result = runner.invoke(cli, ["packages", "happyhorse"])
    assert result.exit_code == 0
    assert "pip install happyhorse-cli" in result.output
    assert "source only" not in result.output
    data = json.loads(runner.invoke(cli, ["packages", "happyhorse", "--json"]).output)
    entry = data["services"][0]
    assert entry["cli_published"] is True
    assert entry["publication_receipt"]["version"] == "2026.10.19.4"
    assert entry["publication_receipt"]["generation_verified"] is False
