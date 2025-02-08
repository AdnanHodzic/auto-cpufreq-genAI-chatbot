# From Zero to AI Hero: How to Build a GenAI Chatbot with Gemini & Vertex AI Agent Builder
# 
# Blog post: https://foolcontrol.org/?p=5051
# Youtube playlist: https://www.youtube.com/watch?list=PL83G0TLSeXRFiTPyctEn_vdL2_Z7xd-e_&v=LgAUPJm4Dio

import os
import requests

# Load the GITHUB_TOKEN from the environment
GITHUB_TOKEN = os.getenv("github_export_token")
if not GITHUB_TOKEN:
    raise ValueError("Environment variable 'github_export_token' is not set. Ensure it is defined and sourced.")

# Repo configuration
REPO_OWNER = "AdnanHodzic"
REPO_NAME = "auto-cpufreq"
OUTPUT_DIR = "./Data/github_issues_html"

# Headers for API authentication
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

# Base API URL
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

def fetch_issues():
    issues = []
    page = 1
    while True:
        response = requests.get(BASE_URL, headers=headers, params={"state": "all", "page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"Failed to fetch issues: {response.status_code} - {response.text}")
            break

        data = response.json()
        if not data:
            break

        issues.extend(data)
        page += 1

    return issues

def fetch_comments(issue_number):
    comments_url = f"{BASE_URL}/{issue_number}/comments"
    response = requests.get(comments_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch comments for issue #{issue_number}: {response.status_code} - {response.text}")
        return []
    return response.json()

def save_issues_as_html(issues):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for issue in issues:
        issue_number = issue["number"]
        title = issue["title"]
        body = issue["body"] or ""
        comments = fetch_comments(issue_number)

        # Prepare the HTML content
        html_content = f"""
        <html>
        <head>
            <title>Issue #{issue_number}: {title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            <p><strong>Issue #{issue_number}</strong></p>
            <div>
                <h2>Description</h2>
                <p>{body}</p>
            </div>
            <div>
                <h2>Comments</h2>
        """
        for comment in comments:
            commenter = comment["user"]["login"]
            comment_body = comment["body"]
            html_content += f"""
                <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
                    <p><strong>{commenter}:</strong></p>
                    <p>{comment_body}</p>
                </div>
            """
        html_content += """
            </div>
        </body>
        </html>
        """

        # Save the HTML file
        with open(f"{OUTPUT_DIR}/issue_{issue_number}.html", "w", encoding="utf-8") as file:
            file.write(html_content)

if __name__ == "__main__":
    print("Fetching issues...")
    issues = fetch_issues()
    print(f"Fetched {len(issues)} issues. Saving to HTML files...")
    save_issues_as_html(issues)
    print(f"Issues saved to {OUTPUT_DIR}")
