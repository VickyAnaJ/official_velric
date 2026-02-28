import unittest

from services.ops_graph.contracts import PolicyConfig
from services.ops_graph.policy import PolicyConfigError, validate_policy_config


class TestPolicyContractValidation(unittest.TestCase):
    def test_valid_config(self):
        config = PolicyConfig(
            allowlisted_actions=("shift_traffic",),
            confidence_threshold=0.8,
            require_approval=False,
        )
        validate_policy_config(config)

    def test_rejects_empty_allowlist(self):
        config = PolicyConfig(
            allowlisted_actions=(),
            confidence_threshold=0.8,
            require_approval=False,
        )
        with self.assertRaises(PolicyConfigError):
            validate_policy_config(config)


if __name__ == "__main__":
    unittest.main()
