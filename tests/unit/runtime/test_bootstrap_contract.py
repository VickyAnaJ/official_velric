import unittest

from services.ops_graph.config import ConfigError, load_config
from tests.support.deterministic import fixed_env


class TestBootstrapContract(unittest.TestCase):
    def test_load_config_success(self):
        cfg = load_config(fixed_env())
        self.assertEqual(cfg.app_env, "development")
        self.assertEqual(cfg.log_level, "info")

    def test_load_config_requires_app_env(self):
        env = fixed_env()
        env["APP_ENV"] = ""
        with self.assertRaises(ConfigError):
            load_config(env)


if __name__ == "__main__":
    unittest.main()
