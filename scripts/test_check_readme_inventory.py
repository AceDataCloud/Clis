"""Catch attribution regressions in the published CLI acquisition paths."""

import unittest

from scripts.check_readme_inventory import attribution_errors, pypi_readme


class AttributionContractTests(unittest.TestCase):
    def setUp(self):
        self.url = (
            "https://platform.acedata.cloud/console/applications?"
            "utm_source=github&utm_medium=referral&utm_campaign=evergreen"
        )

    def test_current_api_key_contract_accepts_html_escaped_query(self):
        text = f"[Get API key]({self.url.replace('&', '&amp;')})"
        self.assertEqual(attribution_errors(text), [])

    def test_package_readme_uses_pypi_for_the_same_entry(self):
        source = f"[Get a key]({self.url})"
        self.assertEqual(attribution_errors(pypi_readme(source), "pypi"), [])
        self.assertIn("utm_source=github", source)
        for literal in [f"`{source}`", f"```md\n{source}\n```", source.replace("platform.acedata.cloud", "platform.acedata.cloud.example")]:
            self.assertEqual(pypi_readme(literal), literal)

    def test_previous_campaign_and_repository_medium_fail(self):
        old = self.url.replace("evergreen", "cli-suno").replace("referral", "repo")
        self.assertTrue(attribution_errors(f"[Get API key]({old})"))

    def test_extra_utm_field_fails(self):
        wrong = self.url + "&utm_extra=value"
        self.assertTrue(attribution_errors(f"[Get API key]({wrong})"))

    def test_duplicate_tags_and_missing_key_entry_fail(self):
        self.assertTrue(attribution_errors(f"[Key]({self.url}&utm_source=github)"))
        self.assertTrue(attribution_errors("No API key entry"))

    def test_unattributed_prose_link_fails_but_api_examples_are_ignored(self):
        key = f"[Key]({self.url})"
        example = "https://platform.acedata.cloud/"
        self.assertTrue(attribution_errors(f"{key}\n[Platform]({example})"))
        self.assertEqual(attribution_errors(f"{key}\n```bash\n{example}\n```\n`{example}`"), [])

    def test_tagged_homepage_cannot_replace_application_entry(self):
        homepage = self.url.replace("/console/applications", "/")
        self.assertTrue(attribution_errors(f"[Key]({homepage})"))


if __name__ == "__main__":
    unittest.main()
