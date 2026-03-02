from .rules import GbThresholdRule, SyntaxSafetyRule


class PolicyEngine:
    def __init__(self, threshold_gb: float):
        self.rules = [
            SyntaxSafetyRule(),
            GbThresholdRule(threshold_gb)
        ]

    def evaluate(self, sql: str, estimated_gb: float, environment: str):
        for rule in self.rules:
            should_block, reason = rule.evaluate(sql, estimated_gb, environment)
            if should_block:
                return True, reason
        return False, None

