import unittest

from tests.support.deterministic import fixed_env, fixed_incident_key


class TestFixtureDeterminism(unittest.TestCase):
    def test_fixed_incident_key_is_stable(self):
        self.assertEqual(fixed_incident_key(7), "incident-0007")
        self.assertEqual(fixed_incident_key(7), "incident-0007")

    def test_fixed_env_is_stable(self):
        self.assertEqual(fixed_env(), fixed_env())


if __name__ == "__main__":
    unittest.main()
