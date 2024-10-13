from transformers import BertTokenizer, BertModel
import torch

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Tokenize the word and get embeddings
word = "king"
inputs = tokenizer(word, return_tensors='pt')
with torch.no_grad():
    outputs = model(**inputs)

# Extract the embedding for the word (BERT gives contextual embeddings, so we take the hidden states)
embedding = outputs.last_hidden_state.mean(dim=1).squeeze()

print(f"Embedding for '{word}':\n", embedding.numpy())
