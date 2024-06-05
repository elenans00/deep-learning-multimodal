import weaviate
import os
import json
import requests
from dotenv import load_dotenv
from huggingface_hub import login
from transformers import AutoModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Load environment variables from .env file
load_dotenv()
# Log in to the Hugging Face Hub using the token
login(token=os.getenv('HUGGINGFACE_TOKEN'))
# Initialize Weaviate client
client = weaviate.Client("http://155.54.95.149:8080")
# Initialize the model for generating embeddings
model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-es', trust_remote_code=True)
# trust_remote_code is needed to use the encode method

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/search")
def search(text_input: str):
    result = process_request(text_input, 10)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    return result 


@app.get("/question")
def question(text_input: str):
    result = process_request(text_input, 3)

    # Prepare the context from the Weaviate query results
    context = '. '.join([item['text'] for item in result['data']['Get']['Video']])
    # Prepare the message for the chat function
    message = {
        "role": "user",
        "content": f"Dado el siguiente contexto: {context}. Responde directamente a la pregunta {text_input}, sin dar más información. Si la respuesta a la pregunta no está en el contexto, solo responde: Desconozco la respuesta a su pregunta, pero debajo puede encontrar vídeos relacionados."
    }
    # Call the chat function with the message
    answer = chat([message])
    # Add the chat answer to the result
    result['data']['Get']['Answer'] = answer['content']

    print(json.dumps(result, indent=4, ensure_ascii=False))
    return result


def process_request(text_input: str, limit: int):
    if not text_input:
        raise HTTPException(status_code=400, detail="text_input cannot be empty")
    
    print ("Text length: ", len(text_input))
    print ("text_input: ", text_input)

    embedding = model.encode(text_input)

    nearVector = {
        "vector": embedding.tolist(),
    }

    result = (client.query.get("Video", 
              ["text", "start", "end", "metadata { filename school_year subject professor class_title }"])
              .with_additional("distance")
              .with_limit(limit) # limit the number of records returned
              .with_near_vector(nearVector).do())

    # Add the URL to the results for using dash in the frontend
    for item in result['data']['Get']['Video']:
        item['url'] = "{}/{}.mpd".format(item['metadata']['filename'],item['metadata']['filename'])

    return result


def chat(messages):
    r = requests.post(
        "http://localhost:11434/api/chat",
        json={"model": "llama3", "messages": messages, "stream": True},
    )
    r.raise_for_status()
    output = ""

    for line in r.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            # the response streams one token at a time, print that as we receive it
            print(content, end="", flush=True)

        if body.get("done", False):
            message["content"] = output
            return message

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
