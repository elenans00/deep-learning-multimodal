import json
import weaviate
import sys
import os
from transformers import AutoModel

# Read the write token from the file
with open("token.txt", "r") as token_file:
    token_read = token_file.read().strip()

# Log in to the Hugging Face Hub using the token
client = weaviate.Client("http://155.54.95.149:8080", token=token_read)

# If a JSON file is not provided, print an error message and exit
if len(sys.argv) < 2:
    print("Usage: ./embeddings.py <json-file>")
    sys.exit(1) 
# Get the JSON file name from the command-line arguments   
json_file = sys.argv[1]
# Extract the base name of the audio file
base_name = os.path.basename(json_file)
# Extract the file name without extension
file_name = os.path.splitext(base_name)[0]

# Load JSON file
try:
    with open(json_file, "r") as file:
        data = json.load(file)     
except Exception as e:  
    print(f"Error loading JSON file: {e}")
    sys.exit(1)

# Initialize the model for generating embeddings
model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-es', trust_remote_code=True)


# METADATA Dhruv ...

# Iterate through each chunk in data and generate embeddings
for chunk in data:
    # Extract text, start time and end time
    text = chunk["text"]
    start_time = chunk["start"]
    end_time = chunk["end"]

    # SIGUIENDO EL ORDEN DE TESTWEAVIATE.PY + DHRUV

    # Encode the text of the chunk to get the embedding
    embedding = model.encode(text)

    # Create an object with the chunk text??? only text???
    data_obj = {
        "text": text,
        "start": start_time,
        "end": end_time
        # METADATA hacer como Dhruv que lo obtiene antes
    }

    # Store the object in Weaviate
    data_uuid = client.data_object.create(
        data_obj,
        "Video",
        vector=embedding
    )
