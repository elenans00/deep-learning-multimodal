#!/home/elena/deep-learning-multimodal/weaviate/venvweaviate/bin/python3
import json
import weaviate
import os
import argparse
from huggingface_hub import login
from transformers import AutoModel

# Main function
def main(input_directory, client, model):

    # Get the list of JSON files in the input directory
    json_files = [f for f in os.listdir(input_directory) if f.endswith('.json')]
    # Make sure that json_files have already not been populated. 
    # Otherwise it will insert duplicate records in weaviate.

    # Process each JSON file
    for file_name in json_files:
        # Create the input file path
        input_file = os.path.join(input_directory, file_name)
        # Read the JSON file
        with open(input_file, "r") as f:
            json_data = json.load(f) 
        
        # Extract metadata from the JSON data
        metadata = json_data["metadata"]
        
        with client.batch(batch_size=100) as batch:
            
            # Iterate through each chunk in json_data and generate embeddings
            for chunk in json_data["chunks"]:
                # Extract text, start time and end time
                text = chunk["text"]
                start_time = chunk["start"]
                end_time = chunk["end"]

                # Encode the text of the chunk to get the embedding
                embedding_video = model.encode(text)

                # Create an object to store the chunk in Weaviate
                data_obj = {
                    "text": text,
                    "start": start_time,
                    "end": end_time,
                    "metadata": metadata 
                }

                # Store the object in Weaviate
                batch.add_data_object(
                    data_obj,
                    "Video",
                    vector=embedding_video
                )

if __name__ == '__main__':
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Generate embeddings from chunks.')
    parser.add_argument('input_directory', type=str, help='Path to the input directory containing JSON files with chunks')
    args = parser.parse_args()

    # Log in to the Hugging Face Hub using the token
    login()
    # Initialize Weaviate client
    client = weaviate.Client("http://155.54.95.149:8080")

    # Initialize the model for generating embeddings
    model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-es', trust_remote_code=True)
    # trust_remote_code is needed to use the encode method

    # Run the extraction
    main(args.input_directory, client, model)