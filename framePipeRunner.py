#framer and piper

import frameExtracter
import frameMediaPiper

# frameExtracter
vidToAnalyze = "New York City School teaching sign language to build more inclusive world (1).mp4"
video_file = f"/Users/sidharthsurapaneni/Desktop/Autonomous Robotics/{vidToAnalyze}"  # Replace with your video file path
frame_output_folder = f"extracted_frames - {vidToAnalyze}"
frameExtracter.extract_frames(video_file, frame_output_folder, frame_rate=3)  # Saves 1 frame every 3 frames

#frameMeidaPiper

piped_output_folder = f"piped frames - {frame_output_folder}"  # Folder where output will be saved
frameMediaPiper.process_all_frames(frame_output_folder, piped_output_folder)

