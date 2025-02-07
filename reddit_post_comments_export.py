import os
import sys
import praw
from praw.models import MoreComments
from datetime import datetime
import re

# Load environment variables
REDDIT_CLIENT_ID = os.getenv("reddit_client_id")
REDDIT_CLIENT_SECRET = os.getenv("reddit_client_secret")
REDDIT_USER_AGENT = "RedditPostDownloader by u/ahodzic"

if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
    raise ValueError("Environment variables 'reddit_client_id' and 'reddit_client_secret' must be set.")

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

def sanitize_filename(title):
    """Sanitize the Reddit post title for use as a filename."""
    return re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')

def fetch_post_and_comments(post_url, output_dir):
    submission = reddit.submission(url=post_url)
    
    # Sanitize post title for filename
    filename = "reddit_" + sanitize_filename(submission.title) + ".html"
    output_path = os.path.join(output_dir, filename)

    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Start building the HTML content
    html_content = f"<html><head><title>{submission.title}</title></head><body>"
    html_content += f"<h1>{submission.title}</h1>"
    html_content += f"<p><em>Posted by u/{submission.author}</em> on {datetime.fromtimestamp(submission.created_utc)}</p>"
    html_content += f"<div><strong>Score:</strong> {submission.score}</div>"
    html_content += f"<div><strong>Content:</strong><br>{submission.selftext_html or submission.url}</div>"
    html_content += "<hr><h2>Comments</h2><ul>"

    # Fetch all comments, including nested ones
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        html_content += format_comment(comment)

    html_content += "</ul></body></html>"

    # Write to file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"Post and comments saved to {output_path}")

def format_comment(comment, depth=0):
    """Recursive function to format a comment and its replies."""
    indent = "&nbsp;" * 4 * depth
    comment_html = f"<li>{indent}<strong>u/{comment.author}:</strong> {comment.body_html or ''}<br>"
    comment_html += f"<small>Score: {comment.score} | Posted on {datetime.fromtimestamp(comment.created_utc)}</small></li>"
    if hasattr(comment, "replies"):
        comment_html += "<ul>"
        for reply in comment.replies:
            comment_html += format_comment(reply, depth + 1)
        comment_html += "</ul>"
    return comment_html

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pipenv run python reddit_post_comments_export.py $Reddit_Post_URL")
        sys.exit(1)

    post_url = " ".join(sys.argv[1:])  # Joins all arguments into a single URL
    output_dir = "Data/reddit_post_comments_html"
    fetch_post_and_comments(post_url, output_dir)
