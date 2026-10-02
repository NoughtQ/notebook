import unittest
from pathlib import Path

from notebook_bot.run import load_config, validate_config


class ConfigTests(unittest.TestCase):
    def test_defaults_are_non_publishing(self):
        config = load_config(Path("notebook_bot/config.json"))
        self.assertEqual(
            (config["mode"], config["daily_limit"], config["author_daily_limit"]),
            ("dry-run", 20, 3),
        )

    def test_publish_requires_model_and_public_paths(self):
        config = load_config(Path("notebook_bot/config.json"))
        with self.assertRaises(ValueError):
            validate_config({**config, "model": "", "public_paths": []}, publish=True)


if __name__ == "__main__":
    unittest.main()
