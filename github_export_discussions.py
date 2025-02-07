import os
import requests

# Load the GITHUB_TOKEN from the environment
GITHUB_TOKEN = os.getenv("github_export_token")
if not GITHUB_TOKEN:
    raise ValueError("Environment variable 'github_export_token' is not set. Ensure it is defined and sourced.")

# Repo configuration
REPO_OWNER = "AdnanHodzic"
REPO_NAME = "auto-cpufreq"
OUTPUT_DIR = "./Data/github_discussions_html"

# Headers for API authentication
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

# Base API URL for Discussions
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/discussions"

def fetch_discussions():
    discussions = []
    page = 1
    while True:
        response = requests.get(BASE_URL, headers=headers, params={"state": "all", "page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"Failed to fetch discussions: {response.status_code} - {response.text}")
            break

        data = response.json()
        if not data:
            break

        discussions.extend(data)
        page += 1

    return discussions

def fetch_comments(discussion_number):
    comments_url = f"{BASE_URL}/{discussion_number}/comments"
    response = requests.get(comments_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch comments for discussion #{discussion_number}: {response.status_code} - {response.text}")
        return []
    return response.json()

def save_discussions_as_html(discussions):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for discussion in discussions:
        discussion_number = discussion["number"]
        title = discussion["title"]
        body = discussion["body"] or ""
        comments = fetch_comments(discussion_number)

        # Prepare the HTML content
        html_content = f"""
        <html>
        <head>
            <title>Discussion #{discussion_number}: {title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            <p><strong>Discussion #{discussion_number}</strong></p>
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
        with open(f"{OUTPUT_DIR}/discussion_{discussion_number}.html", "w", encoding="utf-8") as file:
            file.write(html_content)

if __name__ == "__main__":
    print("Fetching discussions...")
    discussions = fetch_discussions()
    print(f"Fetched {len(discussions)} discussions. Saving to HTML files...")
    save_discussions_as_html(discussions)
    print(f"Discussions saved to {OUTPUT_DIR}")
