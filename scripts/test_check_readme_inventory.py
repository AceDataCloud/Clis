"""Catch attribution regressions in the published CLI acquisition paths."""

import unittest

from scripts.check_readme_inventory import attribution_errors


class AttributionContractTests(unittest.TestCase):
    def setUp(self):
        self.url = (
            "https://platform.acedata.cloud/console/applications?"
            "utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&"
            "utm_content=suno_cli_readme_api_key"
        )

    def test_current_api_key_contract_accepts_html_escaped_query(self):
        text = f"[Get API key]({self.url.replace('&', '&amp;')})"
        self.assertEqual(attribution_errors(text, "suno_cli"), [])

    def test_previous_campaign_and_repository_medium_fail(self):
        old = self.url.replace("evergreen", "cli-suno").replace("referral", "repo")
        self.assertTrue(attribution_errors(f"[Get API key]({old})", "suno_cli"))

    def test_other_service_content_fails(self):
        wrong = self.url.replace("suno_cli", "luma_cli")
        self.assertTrue(attribution_errors(f"[Get API key]({wrong})", "suno_cli"))

    def test_duplicate_tags_and_missing_key_entry_fail(self):
        self.assertTrue(attribution_errors(f"[Key]({self.url}&utm_source=github)", "suno_cli"))
        self.assertTrue(attribution_errors("No API key entry", "suno_cli"))

    def test_unattributed_prose_link_fails_but_api_examples_are_ignored(self):
        key = f"[Key]({self.url})"
        example = "https://platform.acedata.cloud/"
        self.assertTrue(attribution_errors(f"{key}\n[Platform]({example})", "suno_cli"))
        self.assertEqual(attribution_errors(f"{key}\n```bash\n{example}\n```\n`{example}`", "suno_cli"), [])

    def test_tagged_homepage_cannot_replace_application_entry(self):
        homepage = self.url.replace("/console/applications", "/")
        self.assertTrue(attribution_errors(f"[Key]({homepage})", "suno_cli"))


if __name__ == "__main__":
    unittest.main()
