from hypothesis_engine import get_ranked_hypotheses

# ----------------------------------------
# DOCUMENT MAPPING
# (Hypothesis, Service) → Docs
# Use service = "ANY" as fallback
# ----------------------------------------

DOCS_BY_CONTEXT = {
    # -------- AUTH --------
    ("Missing permission", "S3"): [
        {
            "title": "IAM Permissions Overview",
            "url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/access_permissions.html",
            "reason": "Explains how AWS evaluates permissions for actions."
        },
        {
            "title": "S3 Actions and Permissions",
            "url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html",
            "reason": "Lists required permissions for S3 operations like GetObject and PutObject."
        }
    ],

    ("Missing permission", "Lambda"): [
        {
            "title": "Lambda Execution Role",
            "url": "https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html",
            "reason": "Lambda permissions are controlled by its execution role."
        }
    ],

    ("Expired credentials", "ANY"): [
        {
            "title": "Temporary Security Credentials",
            "url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html",
            "reason": "Covers how AWS credentials expire and how to refresh them."
        }
    ],

    # -------- NETWORK --------
    ("Service endpoint unreachable", "EC2"): [
        {
            "title": "Troubleshoot EC2 Connectivity",
            "url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html",
            "reason": "Guides how to diagnose connectivity issues with EC2 instances."
        }
    ],

    ("Security group or firewall blocking traffic", "RDS"): [
        {
            "title": "Troubleshooting Amazon RDS Connectivity",
            "url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Troubleshooting.html",
            "reason": "Explains common causes of database connection failures."
        },
        {
            "title": "Amazon RDS Security Groups",
            "url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.RDSSecurityGroups.html",
            "reason": "Describes how security groups control access to RDS databases."
        }
    ],

    ("Service not available in this region", "ANY"): [
        {
            "title": "AWS Regions and Endpoints",
            "url": "https://docs.aws.amazon.com/general/latest/gr/rande.html",
            "reason": "Resources are isolated per region and may not exist everywhere."
        }
    ],

    # -------- SECURITY --------
    ("Resource is publicly accessible", "S3"): [
        {
            "title": "Block Public Access to Amazon S3",
            "url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html",
            "reason": "Explains how to prevent public access to S3 buckets."
        },
        {
            "title": "S3 Bucket Policies",
            "url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html",
            "reason": "Shows how bucket policies can accidentally allow public access."
        }
    ]
}


# ----------------------------------------
# DOC RECOMMENDER
# ----------------------------------------

def get_docs_for_hypotheses(structured_error, max_hypotheses=2):
    ranked_hypotheses = get_ranked_hypotheses(structured_error, top_n=max_hypotheses)
    service = structured_error.get("service", "ANY")

    recommendations = []

    for h in ranked_hypotheses:
        cause = h["cause"]

        # Try (cause, service) first
        docs = DOCS_BY_CONTEXT.get((cause, service))

        # Fallback to (cause, ANY)
        if not docs:
            docs = DOCS_BY_CONTEXT.get((cause, "ANY"))

        if docs:
            recommendations.append({
                "hypothesis": cause,
                "confidence": h["confidence"],
                "docs": docs
            })

    return recommendations
