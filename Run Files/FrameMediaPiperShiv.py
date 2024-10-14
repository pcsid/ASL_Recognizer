import cv2
import mediapipe as mp
import os
import logging

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

'''
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Disables TensorFlow warnings and errors if used
logging.getLogger('mediapipe').setLevel(logging.ERROR)
'''


# Function to process each frame and run MediaPipe Hands
def process_frame_with_mediapipe(image_path, output_path=None):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to RGB because MediaPipe works with RGB images
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize MediaPipe Hands with static_image_mode=True since we're processing frames
    with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
        # Process the frame to detect hand landmarks
        result = hands.process(image_rgb)

        if result.multi_hand_landmarks:
            with open(output_path, 'w') as f:
                # Iterate through each set of hand landmarks (for each detected hand)
                for hand_index, hand_landmarks in enumerate(result.multi_hand_landmarks):
                    # Create a string to store the landmarks for this hand
                    hand_landmarks_str = ""

                    # Loop through each landmark for the current hand
                    for landmark in hand_landmarks.landmark:
                        # Format each landmark as x, y, z coordinates
                        hand_landmarks_str += f"{landmark.x},{landmark.y},{landmark.z} "

                    # Write the landmarks for the hand to a new line in the file
                    f.write(hand_landmarks_str.strip())  # Strip any extra spaces at the end

                    # If it's not the last hand, add a newline
                    if hand_index < len(result.multi_hand_landmarks) - 1:
                        f.write("\n")

        # # Save or display the processed frame
        # if output_path:
        #     cv2.imwrite(output_path, image)
        # else:
        #     cv2.imshow('MediaPipe Hands', image)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()


# Process all frames in a folder
def process_all_frames(frame_folder, output_folder):
    count = 0
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_files = [f for f in os.listdir(frame_folder) if f.endswith('.jpg')]

    for frame_file in frame_files:
        frame_path = os.path.join(frame_folder, frame_file)
        base_name = os.path.splitext(frame_file)[0]
        output_path = os.path.join(output_folder, f"{base_name}_MediaPipeHands.txt")
        process_frame_with_mediapipe(frame_path, output_path)
    count += 1
    if count % 100 == 0:
        print(f"{count} frames completed")

