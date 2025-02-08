# From Zero to AI Hero: How to Build a GenAI Chatbot with Gemini & Vertex AI Agent Builder
# 
# Blog post: https://foolcontrol.org/?p=5051
# Youtube playlist: https://www.youtube.com/watch?list=PL83G0TLSeXRFiTPyctEn_vdL2_Z7xd-e_&v=LgAUPJm4Dio

import os
import argparse
from googleapiclient.discovery import build
import os

# usage, i.e:
# pipenv run python youtube_comments_downloader.py https://www.youtube.com/watch?v=SPGpkZ0AZVU

# YouTube API Key (read environment variable)
youtube_api_key = os.getenv('youtube_api_key')

# Function to fetch comments from a YouTube video using YouTube API
def fetch_comments(video_url):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)

    video_id = video_url.split('v=')[1]  # Extract video ID from the URL
    comments = []
    
    # Requesting the first page of comments
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=video_id,
        textFormat="plainText"
    )
    
    response = request.execute()

    # Extract comments and replies from the response
    while response:
        for item in response['items']:
            # Top-level comment
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            replies = []

            # Check if there are replies to this comment
            if 'replies' in item:
                for reply in item['replies']['comments']:
                    replies.append(reply['snippet']['textDisplay'])

            comments.append((comment, replies))

        # Check if there are more pages of comments
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                pageToken=response['nextPageToken'],
                textFormat="plainText"
            )
            response = request.execute()
        else:
            break

    return comments

# Function to save comments as an HTML file
def save_comments_as_html(comments, video_title, filename):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Format comments into HTML
    html_content = f"<h1>{video_title} YouTube video comments</h1>\n<ul>\n"
    for comment, replies in comments:
        # Add the top-level comment
        html_content += f"<li>{comment}</li>\n"

        # Add replies as sub-bullets
        if replies:
            html_content += "<ul>\n"
            for reply in replies:
                html_content += f"<li>{reply}</li>\n"
            html_content += "</ul>\n"
    
    html_content += "</ul>\n"

    # Write to the HTML file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"Comments saved as {filename}")

# Fetch video title using YouTube API
def fetch_video_title(video_url):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    video_id = video_url.split('v=')[1]
    
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    
    title = response['items'][0]['snippet']['title']
    return title

def main():
    # usage: pipenv run python youtube_comments_downloader.py URL
    parser = argparse.ArgumentParser(description="Download all comments from a YouTube video and save as HTML")
    parser.add_argument('video_url', help="URL of the YouTube video")
    args = parser.parse_args()

    # Fetch the video title
    video_title = fetch_video_title(args.video_url)

    # Fetch the comments
    comments = fetch_comments(args.video_url)

    # Define output filename
    output_filename = f"Data/youtube_comments/youtube_comments_{video_title.replace(' ', '_')}_comments.html"

    # Save the comments to HTML file
    save_comments_as_html(comments, video_title, output_filename)

if __name__ == "__main__":
    main()
