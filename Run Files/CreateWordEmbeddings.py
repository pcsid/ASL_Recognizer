import torch
from transformers import BertTokenizer, BertModel
import csv
import threading

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def create_and_write_embeddings(video_titles, subtitles, thread_id):

    for i in range(len(video_titles)):

        # Tokenize the entire song lyrics
        inputs = tokenizer(subtitles[i], return_tensors='pt', padding=True, truncation=True)

        # Get the embeddings for each token (word) without gradient calculation
        with torch.no_grad():
            outputs = model(**inputs)

        # Extract the embeddings (last hidden states)
        embeddings = outputs.last_hidden_state

        # Convert token IDs back to words
        tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'].squeeze())

        file_name = "../../WordEmbeddings/" + video_titles[i] + ".txt"

        # Save embeddings to a text file
        with open(file_name, "w") as f:
            for token, embedding in zip(tokens, embeddings.squeeze()):
                f.write(f"Token: {token}\n")
                f.write(f"Embedding: {embedding.numpy().tolist()}\n\n")

    print("Embeddings saved to 'word_embeddings.txt'")

def main_function():
    # Path to your CSV file
    csv_file_path = 'FRI Data List - Sheet1.csv'

    # Initialize arrays to store video titles and subtitles
    video_title_array = []
    subtitle_array = []

    # Open and read the CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Use DictReader to get the column names

        # Iterate through each row and add video titles and subtitles to the arrays
        for row in reader:
            video_title_array.append(row['Video Title'])
            subtitle_array.append(row['Subtitles'])

    # Function to split list into chunks
    def split_list(lst, num_chunks):
        chunk_size = len(lst) // num_chunks
        return [lst[i * chunk_size: (i + 1) * chunk_size] if i != num_chunks - 1 else lst[i * chunk_size:] for i in
                range(num_chunks)]

    # Split video titles and subtitles into thirds
    num_threads = 3
    video_title_chunks = split_list(video_title_array, num_threads)
    subtitle_chunks = split_list(subtitle_array, num_threads)

    # Create and start threads
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=create_and_write_embeddings, args=(video_title_chunks[i], subtitle_chunks[i], i + 1))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All threads have completed.")


main_function()