import csv
from googleapiclient.discovery import build
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import os

# Set up YouTube Data API
API_KEY = 'AIzaSyBOM-Mxca92Tzl6fpvEOdpMaeiDXBBJm6U'  # Replace with your YouTube API key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Function to search for videos
def search_videos(query, max_results):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        type="video"
    ).execute()
    
    video_data = []
    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        video_data.append((video_id, title))
    
    return video_data

# Function to download video using pytube
def download_video(video_id, output_path="../downloads"):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Attempting to download video from URL: {url}")
        yt = YouTube(url)
        
        # Select the highest resolution stream available for download
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if stream:
            stream.download(output_path=output_path)
            print(f"Downloaded video: {yt.title}")
        else:
            print(f"No suitable stream found for video ID: {video_id}")
    except Exception as e:
        print(f"Failed to download video ID {video_id}: {e}")

# Function to retrieve transcript
def get_transcript(video_id, languages=['en']):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        # Format each entry with its start time and text
        transcript_text = "\n".join([f"{entry['start']:.2f} - {entry['text']}" for entry in transcript])
        return transcript_text
    except Exception as e:
        print(f"No transcript available for video ID {video_id}: {e}")
        return None

# Main function to search, download, and retrieve transcripts
def search_and_download_videos(query, max_results, output_path="../downloads"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Search for videos
    video_data = search_videos(query, max_results)
    
    # Prepare CSV file
    csv_file_path = os.path.join(output_path, "video_data.csv")
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Title", "Link", "", "Subtitles"])  # Header row
        
        for video_id, title in video_data:
            # Download the video
            download_video(video_id, output_path)
            
            # Retrieve and save the transcript
            transcript = get_transcript(video_id)
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            csv_writer.writerow([title, video_link, "", transcript])
            print(f"Data saved for video ID: {video_id}")

# Example usage
if __name__ == "__main__":
    search_query = "ASL PSA"
    search_and_download_videos(search_query, max_results=30)
