import cv2
import os

def extract_frames(video_path, output_folder, frame_rate=1):
    """
    Extract frames from a video and save them as images.
    
    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Directory to save the extracted frames.
        frame_rate (int): Number of frames to skip between saved frames (e.g., 1 means save every frame).
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    count = 0
    saved_count = 0

    while success:
        # Save frame every 'frame_rate' frames
        if count % frame_rate == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1

        success, frame = video.read()
        count += 1

    video.release()
    print(f"Extracted {saved_count} frames to {output_folder}")


