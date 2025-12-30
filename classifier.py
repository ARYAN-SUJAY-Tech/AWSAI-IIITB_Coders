def classify_issue(text: str) -> str:
    try:
        text = text.lower()

        # -----------------------------
        # AUTH / IAM
        # -----------------------------
        if any(k in text for k in [
            "accessdenied", "not authorized", "unauthorized",
            "permission", "policy", "iam", "assume role"
        ]):
            return "Authorization / IAM"

        # -----------------------------
        # SECURITY MISCONFIGURATION
        # -----------------------------
        if any(k in text for k in [
            "public access", "publicly accessible",
            "allows public", "exposed to public"
        ]):
            return "Security Misconfiguration"

        # -----------------------------
        # NETWORKING
        # -----------------------------
        if any(k in text for k in [
            "timeout", "timed out", "endpoint",
            "connection refused", "unable to connect",
            "network error"
        ]):
            return "Networking / Connectivity"

        # -----------------------------
        # RESOURCE NOT FOUND
        # -----------------------------
        if any(k in text for k in [
            "not found", "does not exist",
            "no such", "resource not found"
        ]):
            return "Resource Not Found"

        # -----------------------------
        # CONFIG / VALIDATION
        # -----------------------------
        if any(k in text for k in [
            "invalid", "validation", "malformed",
            "missing parameter", "bad request"
        ]):
            return "Configuration / Validation"

        # -----------------------------
        # QUOTAS / LIMITS
        # -----------------------------
        if any(k in text for k in [
            "throttling", "rate exceeded",
            "limit exceeded", "too many requests"
        ]):
            return "Quota / Rate Limits"

        # -----------------------------
        # SERVICE INTEGRATION
        # -----------------------------
        if any(k in text for k in [
            "rds", "dynamodb", "sqs", "sns",
            "unable to connect to database"
        ]):
            return "Service Integration"

        return "General AWS Issue"

    except Exception:
        return "General AWS Issue"
