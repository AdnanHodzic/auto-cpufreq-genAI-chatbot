# From Zero to AI Hero: How to Build a GenAI Chatbot with Gemini & Vertex AI Agent Builder
# 
# Blog post: https://foolcontrol.org/?p=5051
# Youtube playlist: https://www.youtube.com/watch?list=PL83G0TLSeXRFiTPyctEn_vdL2_Z7xd-e_&v=LgAUPJm4Dio

import os
import sys
import youtube_transcript_api
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

# usage, i.e:
# pipenv run python youtube_transcript_downloader.py "https://www.youtube.com/watch?v=SPGpkZ0AZVU"

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    url = url.replace('\\', '')
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            p = parse_qs(parsed_url.query)
            return p.get('v', [None])[0]
    return None

def fetch_video_title(api_key, video_id):
    """Fetch video title using YouTube API."""
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    if "items" in response and len(response["items"]) > 0:
        return response["items"][0]["snippet"]["title"]
    return None

def fetch_transcript(video_id):
    """Fetch the transcript by instantiating the API class."""
    try:
        api_instance = youtube_transcript_api.YouTubeTranscriptApi()
        transcript_list = api_instance.list(video_id)
        transcript = transcript_list.find_transcript(['en']).fetch()
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def format_transcript_to_html(transcript):
    """Format the transcript as HTML using object attributes."""
    html_content = "<h1>Transcript</h1>\n"
    for entry in transcript:
        # Changed from dictionary syntax ['key'] to object syntax .key
        start = entry.start
        duration = entry.duration
        text = entry.text
        html_content += f"<p><strong>{start:.2f} - {start + duration:.2f} seconds:</strong> {text}</p>\n"
    return html_content

def save_transcript_as_html(transcript, video_title, filename):
    """Save the transcript as an HTML file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    formatted_transcript = format_transcript_to_html(transcript)
    html_content = f"<h1>{video_title} YouTube video transcript</h1>\n"
    html_content += formatted_transcript
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"Transcript saved as {filename}")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcript_downloader.py <YouTube Video URL>")
        sys.exit(1)

    video_url = sys.argv[1]
    video_id = get_video_id(video_url)

    if not video_id:
        print(f"Invalid YouTube URL: {video_url}")
        sys.exit(1)

    api_key = os.getenv("youtube_api_key")
    if not api_key:
        print("Error: Please set your youtube_api_key as an environment variable.")
        sys.exit(1)

    video_title = fetch_video_title(api_key, video_id)
    if not video_title:
        print("Error fetching video title")
        sys.exit(1)

    transcript = fetch_transcript(video_id)
    if not transcript:
        print("No transcript found")
        sys.exit(1)

    safe_title = "".join([c for c in video_title if c.isalnum() or c in (' ', '_')]).rstrip()
    output_filename = f"Data/youtube_transcripts/youtube_transcript_{safe_title.replace(' ', '_')}_transcript.html"
    save_transcript_as_html(transcript, video_title, output_filename)

if __name__ == "__main__":
    main()