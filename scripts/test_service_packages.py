"""Prevent unsafe promotion or ambiguous ownership in the service directory."""

import copy
import json
import unittest

from scripts.service_packages import ROOT, bundled, validate


class ServicePackageDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "service-packages.json").read_text())

    def test_current_catalog_is_valid_and_bundled(self):
        self.assertEqual(validate(self.data), [])
        self.assertEqual(
            (ROOT / "adc/adc_cli/service_packages.json").read_text(), bundled(self.data)
        )

    def test_unpublished_happyhorse_requires_new_receipt(self):
        data = copy.deepcopy(self.data)
        entry = next(item for item in data["services"] if item["slug"] == "happyhorse")
        entry.pop("publication_receipt", None)
        self.assertTrue(validate(data))

    def test_third_party_package_identity_is_not_an_ace_repository(self):
        data = copy.deepcopy(self.data)
        data["services"][0]["mcp_repo"] = "https://github.com/another-publisher/suno"
        self.assertTrue(validate(data))

    def test_duplicate_service_identity_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["services"].append(data["services"][0])
        self.assertTrue(validate(data))


class ServiceProfileTests(unittest.TestCase):
    def test_gpt_image_cannot_silently_become_generic_openai(self):
        data = json.loads((ROOT / "service-packages.json").read_text())
        entry = next(item for item in data["services"] if item["slug"] == "gpt-image")
        entry["mcp_arguments"] = ["mcp-openai-pro"]
        self.assertTrue(validate(data))


class PublicationReceiptTests(unittest.TestCase):
    def test_happyhorse_requires_both_official_artifact_hashes(self):
        data = json.loads((ROOT / "service-packages.json").read_text())
        entry = next(item for item in data["services"] if item["slug"] == "happyhorse")
        entry["publication_receipt"]["artifacts"][0]["sha256"] = "not-a-valid-hash"
        self.assertTrue(validate(data))

    def test_receipt_cannot_point_to_an_unrelated_registry_project(self):
        data = json.loads((ROOT / "service-packages.json").read_text())
        entry = next(item for item in data["services"] if item["slug"] == "happyhorse")
        entry["publication_receipt"]["official_metadata_url"] = (
            "https://pypi.org/pypi/another-package/1/json"
        )
        self.assertTrue(validate(data))
