class GbThresholdRule:
    def __init__(self, threshold_gb: float):
        self.threshold_gb = threshold_gb

    def evaluate(self, sql: str, estimated_gb: float, environment: str):
        if estimated_gb > self.threshold_gb:
            return True, f"Estimated {estimated_gb}GB exceeds threshold {self.threshold_gb}GB"
        return False, None


class SyntaxSafetyRule:
    def evaluate(self, sql: str, estimated_gb: float, environment: str):
        dangerous_keywords = ["DELETE", "DROP", "TRUNCATE"]

        if environment.lower() == "prod":
            upper_sql = sql.upper()
            for keyword in dangerous_keywords:
                if keyword in upper_sql:
                    return True, f"{keyword} not allowed in PROD"

        return False, None
