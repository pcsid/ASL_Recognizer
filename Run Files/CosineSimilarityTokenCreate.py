import torch
import torch.nn.functional as F
import os
import threading

def read_landmarks_from_file(file_path, output_file, dir_name):

    two_hand_landmark_list = []

    with open(file_path, 'r') as file:
        # Read the file line by line
        for line in file:
            landmarks_list = []

            # Split the line into individual coordinate values using commas
            values = line.split(' ')

            # Group the values into (x, y, z) sets
            for land_mark in values:
                split_land_mark = land_mark.split(',')
                x = float(split_land_mark[0])
                y = float(split_land_mark[1])
                z = float(split_land_mark[2])

                landmarks_list.append([x, y, z])
            two_hand_landmark_list.append(landmarks_list)

    cosine_similarity_list_two_hand = []
    for landmarks_list in two_hand_landmark_list:
        cosine_similarity_list_two_hand.append(calculate_cosine_similarities(landmarks_list))

    new_directory_path = "../../ExtractedMediaPipeHands/CosineSimilarities/" + dir_name
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)

    new_cosine_similarity_file = "../../ExtractedMediaPipeHands/CosineSimilarities/" + dir_name + "/" + os.path.splitext(output_file)[0] + "_CosineSimilarity.txt"

    # Output the cosine similarity results
    with open(new_cosine_similarity_file, 'w') as f:
        for cos_sim in cosine_similarity_list_two_hand:
            f.write(f"{cos_sim}\n")  # Write each similarity on a new line


def calculate_cosine_similarities(landmarks):
    # List of pairs to compute cosine similarity between
    landmark_pairs = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (0, 9), (9, 10), (10, 11), (11, 12),
        (0, 13), (13, 14), (14, 15), (15, 16),
        (0, 17), (17, 18), (18, 19), (19, 20)
    ]

    # Convert the 2D list of landmarks into PyTorch tensors
    landmarks_tensor = torch.tensor(landmarks)

    # Initialize a list to store the cosine similarity results
    cosine_similarities = []

    # Compute cosine similarity for each pair
    for pair in landmark_pairs:
        idx1, idx2 = pair
        if idx1 < len(landmarks_tensor) and idx2 < len(landmarks_tensor):
            # Select the two landmark tensors
            landmark1 = landmarks_tensor[idx1]
            landmark2 = landmarks_tensor[idx2]

            # Compute cosine similarity between the two landmarks
            cos_sim = F.cosine_similarity(landmark1.unsqueeze(0), landmark2.unsqueeze(0))

            # Append the result to the list
            cosine_similarities.append(cos_sim.item())
        else:
            print(f"Warning: Index out of bounds for pair {pair}")

    return cosine_similarities


def process_directories(directory_names, thread_id):
    extracted_media_pipe_hands_directory = "../../ExtractedMediaPipeHands"

    for dir_name in directory_names:
        dir_path = os.path.join(extracted_media_pipe_hands_directory, dir_name)

        # List all file names in the current directory
        file_names = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        file_paths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if
                      os.path.isfile(os.path.join(dir_path, f))]

        dir_name_new = dir_name + "_CosineSimilarities"

        for file_name in file_names:
            file_name_w_path = os.path.join(dir_path, file_name)
            read_landmarks_from_file(file_name_w_path, file_name, dir_name_new)

def run_function():
    extracted_media_pipe_hands_directory = "../../ExtractedMediaPipeHands"

    directory_names = [d for d in os.listdir(extracted_media_pipe_hands_directory)
                       if os.path.isdir(os.path.join(extracted_media_pipe_hands_directory, d))]

    total_directories = len(directory_names)
    chunk_size = total_directories // 3

    # Divide into three chunks
    chunk1 = directory_names[:chunk_size]
    chunk2 = directory_names[chunk_size:2 * chunk_size]
    # The third chunk gets the remainder
    chunk3 = directory_names[2 * chunk_size:]

    # Create and start threads
    thread1 = threading.Thread(target=process_directories, args=(chunk1, 1))
    thread2 = threading.Thread(target=process_directories, args=(chunk2, 2))
    thread3 = threading.Thread(target=process_directories, args=(chunk3, 3))

    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to complete
    thread1.join()
    thread2.join()
    thread3.join()

    print("All threads have completed.")


# Example usage:


