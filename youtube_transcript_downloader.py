# From Zero to AI Hero: How to Build a GenAI Chatbot with Gemini & Vertex AI Agent Builder
# 
# Blog post: https://foolcontrol.org/?p=5051
# Youtube playlist: https://www.youtube.com/watch?list=PL83G0TLSeXRFiTPyctEn_vdL2_Z7xd-e_&v=LgAUPJm4Dio

import os
import sys
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build

# usage, i.e:
# pipenv run python youtube_transcript_downloader.py https://www.youtube.com/watch?v=SPGpkZ0AZVU

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    if "v=" in url:
        return url.split("v=")[1]
    return None

def fetch_video_title(api_key, video_id):
    """Fetch video title using YouTube API."""
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    if "items" in response:
        return response["items"][0]["snippet"]["title"]
    return None

def fetch_transcript(video_id):
    """Fetch the transcript for the video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def format_transcript_to_html(transcript):
    """Format the transcript as HTML."""
    html_content = "<h1>Transcript</h1>\n"
    for entry in transcript:
        html_content += f"<p><strong>{entry['start']:.2f} - {entry['start'] + entry['duration']:.2f} seconds:</strong> {entry['text']}</p>\n"
    return html_content

def save_transcript_as_html(transcript, video_title, filename):
    """Save the transcript as an HTML file."""
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Format the transcript to HTML
    formatted_transcript = format_transcript_to_html(transcript)

    # Add video title at the top
    html_content = f"<h1>{video_title} YouTube video transcript</h1>\n"
    html_content += formatted_transcript

    # Write to the HTML file
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
        print("Invalid YouTube URL")
        sys.exit(1)

    # Fetch the video title
    api_key = os.getenv("youtube_api_key")
    if not api_key:
        raise ValueError("Please set your YOUTUBE_API_KEY as an environment variable.")

    video_title = fetch_video_title(api_key, video_id)
    if not video_title:
        print("Error fetching video title")
        sys.exit(1)

    # Fetch the transcript
    transcript = fetch_transcript(video_id)
    if not transcript:
        print("No transcript found")
        sys.exit(1)

    # Save transcript as HTML
    output_filename = f"Data/youtube_transcripts/youtube_transcript_{video_title.replace(' ', '_')}_transcript.html"
    save_transcript_as_html(transcript, video_title, output_filename)

if __name__ == "__main__":
    main()
