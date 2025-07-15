import os
import requests
import time

# Mock token info (replace with dynamic logic later)
token = {"name": "splunk-token-production"}
grace_period = 45
ttl = 365

# Build issue content
token_name = token.get("name")
issue_body = f"""\
**Token Name**: {token_name}
**Grace Period**: {grace_period}
**TTL**: {ttl}
"""

issue_payload = {
    "title": f"🔁 Rotate Splunk Token: {token_name}",
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

# 3. Close issue
close_resp = requests.patch(
    f"https://api.github.com/repos/{repo}/issues/{issue_number}",
    headers=headers,
    json={"state": "closed"}
)

if close_resp.status_code == 200:
    print(f"Issue #{issue_number} closed.")
else:
    print("❌ Failed to close issue:", close_resp.status_code, close_resp.text)
