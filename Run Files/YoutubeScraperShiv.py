from pytubefix import YouTube
from pytubefix.cli import on_progress
import csv
import threading


def get_links_from_csv():
    video_links = []

    # Read the CSV file
    with open('FRI Data List - Sheet1.csv', mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            video_links.append(row['Video Link'])

    return video_links

def create_threads():
    # Get the full list of videos (assuming it's 33 videos)
    total_video_list = get_links_from_csv()

    # Calculate the number of videos per thread (in this case 11 each)
    num_videos_per_thread = len(total_video_list) // 3

    # Create slices for each thread
    video_list_1 = total_video_list[:num_videos_per_thread]
    video_list_2 = total_video_list[num_videos_per_thread:num_videos_per_thread * 2]
    video_list_3 = total_video_list[num_videos_per_thread * 2:]

    # Create and start threads
    thread1 = threading.Thread(target=download_videos, args=(video_list_1,))
    thread2 = threading.Thread(target=download_videos, args=(video_list_2,))
    thread3 = threading.Thread(target=download_videos, args=(video_list_3,))

    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to complete
    thread1.join()
    thread2.join()
    thread3.join()

    print("Downloaded everything")

def download_videos(video_list):
    for url in video_list:
        try:
            yt = YouTube(url, on_progress_callback=on_progress)
            print(f"Downloading: {yt.title}")

            # Get the highest resolution stream
            ys = yt.streams.get_highest_resolution()

            # Download the video
            ys.download(output_path="../../VideoDownloads") # REPLACE THIS FILE WITH WHEREVER YOU WANT TO DOWNLOAD THE VIDEOS
            print(f"Downloaded: {yt.title}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")


#create_threads()

# Missing - Good now Manually Downloaded
# https://www.youtube.com/watch?v=LddambSDw2s&ab_channel=AmberGProductions
# https://www.youtube.com/watch?v=GHcdoGeF6sQ&ab_channel=AmberGProductions
# https://www.youtube.com/watch?v=-NnMx5VDQGs&ab_channel=AmberGProductions
# https://www.youtube.com/watch?v=CR9k8mQ9dPE&ab_channel=AmberGProductions