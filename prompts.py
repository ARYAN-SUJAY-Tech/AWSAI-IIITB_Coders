import re

def parse_aws_error(error_text: str) -> dict:
    error = {
        "raw_error": error_text,
        "error_code": None,
        "service": None,
        "category": None,
        "action": None,
        "resource": None,
        "identity": None,
        "region": None,
        "is_retryable": False
    }

    text = error_text.lower()

    # -------------------------------------------------
    # ERROR CODE (more inclusive)
    # -------------------------------------------------
    code_match = re.search(
        r'(AccessDenied|Unauthorized|NotAuthorized|ValidationException|ThrottlingException|[A-Za-z]+Exception)',
        error_text
    )
    if code_match:
        error["error_code"] = code_match.group(1)

    # -------------------------------------------------
    # CATEGORY DETECTION (expanded & ordered)
    # -------------------------------------------------
    if any(k in text for k in ["accessdenied", "unauthorized", "notauthorized"]):
        error["category"] = "Auth"

    elif any(k in text for k in ["timeout", "timed out", "connection refused", "unable to connect", "endpoint"]):
        error["category"] = "Network"
        error["is_retryable"] = True

    elif any(k in text for k in ["notfound", "no such", "does not exist"]):
        error["category"] = "Resource"

    elif any(k in text for k in ["invalid", "validation", "malformed", "missing parameter"]):
        error["category"] = "Config"

    elif any(k in text for k in ["throttling", "rate exceeded", "limit exceeded"]):
        error["category"] = "Quota"
        error["is_retryable"] = True

    elif any(k in text for k in ["public access", "publicly accessible", "allows public"]):
        error["category"] = "Security"

    # -------------------------------------------------
    # ACTION (service:Action pattern)
    # -------------------------------------------------
    action_match = re.search(r'([a-z0-9]+:[A-Za-z]+)', error_text)
    if action_match:
        error["action"] = action_match.group(1)
        error["service"] = action_match.group(1).split(":")[0].upper()

    # -------------------------------------------------
    # SERVICE FALLBACK (keyword-based)
    # -------------------------------------------------
    if not error["service"]:
        if "s3" in text or "bucket" in text:
            error["service"] = "S3"
        elif "lambda" in text:
            error["service"] = "Lambda"
        elif "ec2" in text or "endpoint" in text:
            error["service"] = "EC2"
        elif "rds" in text or "database" in text:
            error["service"] = "RDS"

    # -------------------------------------------------
    # RESOURCE (ARN or generic)
    # -------------------------------------------------
    arn_match = re.search(r'(arn:aws:[^\s]+)', error_text)
    if arn_match:
        error["resource"] = arn_match.group(1)

    # -------------------------------------------------
    # IDENTITY (strict word boundaries)
    # -------------------------------------------------
    if re.search(r'\buser\b', text):
        error["identity"] = "User"
    elif re.search(r'\brole\b', text):
        error["identity"] = "Role"

    # -------------------------------------------------
    # REGION
    # -------------------------------------------------
    region_match = re.search(r'([a-z]{2}-[a-z]+-\d)', error_text)
    if region_match:
        error["region"] = region_match.group(1)

    return error


def extract_error_block(user_text: str) -> str:
    lines = user_text.splitlines()

    # Prefer lines that look like errors
    candidates = [
        line for line in lines
        if any(k in line for k in [
            "Exception", "Error", "AccessDenied", "NotAuthorized",
            "NotFound", "Validation", "Throttling"
        ])
    ]

    # If we found something, join nearby lines
    if candidates:
        return " ".join(candidates)

    # Fallback: return original text
    return user_text


def build_prompt(user_input: str, issue_type: str) -> str:
    user_input = parse_aws_error(extract_error_block(user_input))
    return f"""
You are an experienced AWS Support Engineer.

Issue Category: {issue_type}

User Input:
{user_input}

-----------------------------
OUTPUT FORMAT (STRICT)
-----------------------------

### 🔴 Problem Summary
Explain what is failing and which AWS service is involved.

### 🧠 Root Cause
Explain why this happens in simple language.

### 🛠️ How to Fix (Step-by-Step)
Give exact AWS Console steps.

### ⚠️ Common Beginner Mistake
Explain a typical misunderstanding.

### 🔐 Security Note
Mention least-privilege best practices.
Do NOT suggest Action:"*" or Resource:"*".

-----------------------------
RULES
-----------------------------
- Beginner-friendly language
- AWS-specific terminology
- No hallucinated services
- Be concise and accurate
"""
