import os
from frameExtracter import extract_frames
from FrameMediaPiperShiv import process_all_frames
import threading

def extract_all_frames_for_every_video_in_directory():
    # Directory paths
    video_dir = '../../VideoDownloads/'
    extracted_frames_dir = '../../ExtractedFrames/'

    # Get list of all files in the video directory
    file_names = os.listdir(video_dir)

    # Filter out any non-file entries (e.g., directories)
    file_names = [f for f in file_names if os.path.isfile(os.path.join(video_dir, f))]

    # Loop through each file and call extract_frames with the required parameters
    for file_name in file_names:
        input_file_path = os.path.join(video_dir, file_name)
        output_dir = os.path.join(extracted_frames_dir, f"{file_name}_ExtractedFrames")

        # Call the extract_frames function with the file path and output directory
        extract_frames(input_file_path, output_dir, frame_rate=3)


def apply_media_pipe_hands_to_all_extracted_frames():

    # Define the directories
    extracted_frames_dir = '../../ExtractedFrames/'
    output_base_dir = '../../ExtractMediaPipeHands/'

    # List all directory names in the extracted_frames_dir
    directory_names = [os.path.join(extracted_frames_dir, d) for d in os.listdir(extracted_frames_dir)
                       if os.path.isdir(os.path.join(extracted_frames_dir, d))]

    # Function to process directories in a chunk
    def process_directory_chunk(directory_chunk):
        for directory in directory_chunk:
            output_dir = os.path.join(output_base_dir, f"{directory}_MediaPipeHands")
            process_all_frames(directory, output_dir)

    # Split the directory_names into 3 chunks
    chunk_size = 11
    chunks = [directory_names[i:i + chunk_size] for i in range(0, len(directory_names), chunk_size)]

    # Create and start 3 threads, each handling a chunk
    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=process_directory_chunk, args=(chunk,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All threads have completed.")


apply_media_pipe_hands_to_all_extracted_frames()