import os
import requests
import time

# Mock token info (replace with dynamic logic later)
token = {"name": "splunk-token-production"}
grace_period = 45
ttl = 365

token_name = token.get("name")
grace_period = 45
ttl = 365

issue_body = f"""\
**token_name**  
{token_name}

**grace_period**  
{grace_period}

**token_expiry_length**  
{ttl}
"""

issue_payload = {
    "title": f"splunk-observability token management",
    "body": issue_body
}

# Read GitHub token and repo from env
gh_token = os.environ["GH_TOKEN"]
repo = os.environ["GITHUB_REPOSITORY"]

headers = {
    "Authorization": f"token {gh_token}",
    "Accept": "application/vnd.github+json"
}

# 1. Create issue
create_resp = requests.post(
    f"https://api.github.com/repos/{repo}/issues",
    headers=headers,
    json=issue_payload
)

if create_resp.status_code == 201:
    issue = create_resp.json()
    issue_number = issue["number"]
    print(f"Issue #{issue_number} created: {issue['html_url']}")
else:
    print("❌ Failed to create issue:", create_resp.status_code, create_resp.text)
    exit(1)

# 2. Optional: Pause before closing
time.sleep(3)


def trigger_next_workflow(event_type, payload):
    headers = {
        "Authorization": f"token {gh_token}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.post(
        f"https://api.github.com/repos/{repo}/dispatches",
        json={
            "event_type": event_type,
            "client_payload": payload
        },
        headers=headers
    )
    response.raise_for_status()

    if response.status_code != 204:
        return False

    return True

# 3. Close issue
close_resp = requests.patch(
    f"https://api.github.com/repos/{repo}/issues/{issue_number}",
    headers=headers,
    json={"state": "closed"}
)

if close_resp.status_code == 200:
    print(f"Issue #{issue_number} closed.")
    print(f"Trigger other workflow")
    trigger_next_workflow("trigger-next-job", {"issue": issue_number})

else:
    print("❌ Failed to close issue:", close_resp.status_code, close_resp.text)
