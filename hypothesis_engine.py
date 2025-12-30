# -----------------------------
# AUTHORIZATION ERRORS
# -----------------------------
AUTH_HYPOTHESES = [
    {"name": "Missing permission", "base": 0.4},
    {"name": "Wrong identity", "base": 0.25},
    {"name": "Expired credentials", "base": 0.2},
    {"name": "Explicit deny policy", "base": 0.15},
]

def score_auth_hypotheses(structured_error):
    scores = {h["name"]: h["base"] for h in AUTH_HYPOTHESES}

    # Strong signal: AccessDenied / Unauthorized
    if structured_error["error_code"] in ["AccessDenied", "AccessDeniedException", "Unauthorized", "NotAuthorized"]:
        scores["Missing permission"] += 0.2

    # Action present → permission likely
    if structured_error["action"]:
        scores["Missing permission"] += 0.1

    # Identity present → creds likely valid
    if structured_error["identity"]:
        scores["Expired credentials"] -= 0.1

    return scores


# -----------------------------
# NETWORK ERRORS
# -----------------------------
NETWORK_HYPOTHESES = [
    {"name": "Service endpoint unreachable", "base": 0.4},
    {"name": "Security group or firewall blocking traffic", "base": 0.35},
    {"name": "Service not available in this region", "base": 0.25},
]

def score_network_hypotheses(structured_error):
    scores = {h["name"]: h["base"] for h in NETWORK_HYPOTHESES}

    # Timeout / connection refused → endpoint or network path
    if structured_error["is_retryable"]:
        scores["Service endpoint unreachable"] += 0.15

    # RDS / database hints → SG issues
    if structured_error["service"] == "RDS":
        scores["Security group or firewall blocking traffic"] += 0.15

    # Region known → reduce region mismatch
    if structured_error["region"]:
        scores["Service not available in this region"] -= 0.1

    return scores


# -----------------------------
# SECURITY FINDINGS
# -----------------------------
SECURITY_HYPOTHESES = [
    {"name": "Resource is publicly accessible", "base": 0.6},
    {"name": "Policy misconfiguration", "base": 0.4},
]

def score_security_hypotheses(structured_error):
    scores = {h["name"]: h["base"] for h in SECURITY_HYPOTHESES}

    if structured_error["service"] == "S3":
        scores["Resource is publicly accessible"] += 0.1

    return scores


# -----------------------------
# ROUTER
# -----------------------------
def get_ranked_hypotheses(structured_error, top_n=3):
    category = structured_error.get("category")

    if category == "Auth":
        scores = score_auth_hypotheses(structured_error)

    elif category == "Network":
        scores = score_network_hypotheses(structured_error)

    elif category == "Security":
        scores = score_security_hypotheses(structured_error)

    else:
        return []

    return normalize_and_rank(scores, top_n)


# -----------------------------
# NORMALIZATION
# -----------------------------
def normalize_and_rank(scores, top_n=3):
    total = sum(max(v, 0) for v in scores.values())

    ranked = [
        {"cause": k, "confidence": round(v / total, 2)}
        for k, v in scores.items()
        if v > 0
    ]

    ranked.sort(key=lambda x: x["confidence"], reverse=True)
    return ranked[:top_n]
