import os
import requests
import time

# Load GH token and repo info from env
gh_token = os.environ["GH_TOKEN"]
repo = os.environ["GITHUB_REPOSITORY"]

headers = {
    "Authorization": f"token {gh_token}",
    "Accept": "application/vnd.github+json"
}

# 1. Create an issue
issue_data = {
    "title": "🔧 Test Issue from GitHub Actions",
    "body": "This issue was created by a Python script using GH_TOKEN."
}

create_resp = requests.post(
    f"https://api.github.com/repos/{repo}/issues",
    headers=headers,
    json=issue_data
)

if create_resp.status_code == 201:
    issue = create_resp.json()
    issue_number = issue["number"]
    print(f"Issue #{issue_number} created: {issue['html_url']}")
else:
    print("Failed to create issue:", create_resp.text)
    exit(1)

# 2. Wait 3 seconds before closing (just for demo)
time.sleep(3)

# 3. Close the issue
close_resp = requests.patch(
    f"https://api.github.com/repos/{repo}/issues/{issue_number}",
    headers=headers,
    json={"state": "closed"}
)

if close_resp.status_code == 200:
    print(f"Issue #{issue_number} closed.")
else:
    print("Failed to close issue:", close_resp.text)
