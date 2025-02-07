import os
import base64
import requests
from markdown2 import markdown

# Define repository URL and GitHub API token
repo_url = "https://github.com/AdnanHodzic/auto-cpufreq"
GITHUB_TOKEN = os.getenv("github_export_token")

# Function to get README content from GitHub API
def get_readme_content(repo_url, token):
    # Correctly format the API URL
    repo_api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/") + "/contents/README.md"
    
    # Print the API URL for debugging
    print(f"Fetching README from URL: {repo_api_url}")
    
    headers = {
        "Authorization": f"token {token}"
    }
    response = requests.get(repo_api_url, headers=headers)
    
    if response.status_code == 200:
        content = response.json()
        return base64.b64decode(content['content']).decode('utf-8')
    else:
        print(f"Error fetching README: {response.status_code} - {response.json()}")
        return None

# Function to convert Markdown to HTML
def convert_markdown_to_html(markdown_content):
    try:
        return markdown(markdown_content)
    except Exception as e:
        print(f"Error converting to HTML: {e}")
        return None

# Main function
def export_readme_as_html(repo_url, token):
    print("GitHub token loaded.")
    
    # Get README content
    readme_content = get_readme_content(repo_url, token)
    
    if readme_content:
        # Convert to HTML
        html_content = convert_markdown_to_html(readme_content)
        
        if html_content:
            # Save to HTML file
            output_dir = "./Data/github_readme_html"
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, "README.html")
            
            try:
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(html_content)
                print(f"README content successfully saved as HTML: {output_file}")
            except Exception as e:
                print(f"Error saving HTML file: {e}")
        else:
            print("No HTML content to save.")
    else:
        print("Failed to fetch README content.")

# Execute the script
export_readme_as_html(repo_url, GITHUB_TOKEN)
