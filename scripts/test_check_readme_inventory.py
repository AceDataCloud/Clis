#!/usr/bin/env python3
from __future__ import annotations

import unittest

from check_readme_inventory import acquisition_url, main


class AcquisitionInventoryTest(unittest.TestCase):
    def test_campaign_gets_stable_url(self) -> None:
        self.assertEqual(
            acquisition_url("cli-suno"),
            "https://platform.acedata.cloud/?utm_source=github&utm_medium=repo&utm_campaign=cli-suno",
        )

    def test_invalid_campaign_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            acquisition_url("CLI Suno")

    def test_repository_inventory_is_valid(self) -> None:
        self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
