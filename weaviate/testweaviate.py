#!/home/elena/deep-learning-multimodal/weaviate/venvweaviate/bin/python3
import json
import weaviate
import os
import argparse
from huggingface_hub import login
from transformers import AutoModel

# Main function
def main(client, model): #n_records aqui o ver abajo para limite de 10!!

    # Hacemos búsqueda concreta para prueba
    emb = model.encode("clase del viernes 29 de abril")

    nearVector = {
        "vector": emb.tolist(),
    }

    result = (client.query.get("Video", 
              ["text", "start", "end", "metadata { filename }"])
              .with_additional("distance")
              .with_limit(10) # limit the number of records returned
              .with_near_vector(nearVector).do())
    
    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    # Log in to the Hugging Face Hub using the token
    login()
    # Initialize Weaviate client
    client = weaviate.Client("http://155.54.95.149:8080")

    # Initialize the model for generating embeddings
    model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-es', trust_remote_code=True)
    # trust_remote_code is needed to use the encode method

    # Run the extraction
    main(client, model)