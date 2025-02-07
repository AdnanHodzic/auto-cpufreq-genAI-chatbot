import os
import requests
import json

# Define repository URL and GitHub API token
REPO_URL = "https://api.github.com/repos/AdnanHodzic/auto-cpufreq" 
GITHUB_TOKEN = os.getenv("github_export_token")

if not GITHUB_TOKEN:
    raise ValueError("Environment variable 'github_export_token' is not set. Ensure it is defined and sourced.")

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
OUTPUT_DIR = "./Data/github_releases_html"

# Function to fetch releases from GitHub
def get_releases():
    url = f"{REPO_URL}/releases"
    releases = []
    page = 1
    while True:
        response = requests.get(url, headers=HEADERS, params={'page': page, 'per_page': 100})
        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            releases.extend(data)
            page += 1
        else:
            print(f"Error fetching releases: {response.status_code} - {response.json()}")
            break
    return releases

# Convert releases data to HTML with improved formatting
def convert_releases_to_html(releases):
    html_content = "<h1>Releases</h1>"
    
    for release in releases:
        html_content += f"<h2>{release['name']} ({release['tag_name']})</h2>"
        html_content += f"<p><strong>Published on:</strong> {release['published_at']}</p>"

        # Add description with bullet points if available
        description = release.get('body', 'No description available.')
        if description:
            html_content += "<p><strong>Description:</strong></p>"
            html_content += "<ul>"
            # Split description by lines and check if any line starts with a bullet point
            for line in description.split('\n'):
                if line.strip().startswith('*'):  # If it's a bullet point, use <li>
                    html_content += f"<li>{line.strip('*').strip()}</li>"
                else:
                    html_content += f"<p>{line}</p>"  # Other text content
            html_content += "</ul>"
        else:
            html_content += "<p>No detailed description available.</p>"

        html_content += f"<p><strong>URL:</strong> <a href='{release['html_url']}'>Release Link</a></p>"
        html_content += "<hr>"

    return html_content

# Save content to HTML file
def save_to_html(filename, content):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as file:
        file.write(content)

# Main function to export releases to HTML
def main():
    print("GitHub token loaded.")
    
    # Fetch releases from GitHub
    releases = get_releases()

    # Convert releases to HTML
    html_content = convert_releases_to_html(releases)

    # Save the HTML content to a file
    save_to_html("releases.html", html_content)
    print("Releases saved as HTML.")

if __name__ == "__main__":
    main()
