import re

def should_escalate(incoming_issue):
    if incoming_issue["priority"] == "high":
        # Combine all tags into one string
        tags_combined = " ".join([incoming_issue[f"tag_{i+1}"] for i in range(9)])

        # Keywords that trigger escalation
        keywords = ["Disruption","urgent","issue","refund", "Failure", "Outage", "Incident", "Crash", "Breach", "Critical"]

        # Check if any keyword matches in the combined tags using regular expressions for whole word matching
        for key in keywords:
            if re.search(r'\b' + re.escape(key.lower()) + r'\b', tags_combined.lower()):
                return True

    return False