## Comprobamos que funciona la conexión con la BBDD
import weaviate
from huggingface_hub import login
login()
from transformers import AutoModel
client = weaviate.Client("http://155.54.95.149:8080")
client.schema.get()

## Comprobamos que podemos generar los embeddings
model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-es', trust_remote_code=True) # trust_remote_code is needed to use the encode method

# Creamos objeto con primera frase
data_obj = {
    "frase": "Hello from the moon!"
}
embedding = model.encode(data_obj["frase"])

data_uuid = client.data_object.create(
  data_obj,
  "YourClass",
  vector=embedding
)

# Creamos objeto con la segunda frase
data_obj2 = {
    "frase": "I'm an apple!"
}
embedding2 = model.encode(data_obj2["frase"])

data_uuid2 = client.data_object.create(
  data_obj2,
  "YourClass",
  vector=embedding2
)

# Hacemos la búsqueda
emb3 = model.encode("I'm an apple")

nearVector = {
    "vector": emb3.tolist(),
}

result = (client.query.get("YourClass", "frase").with_additional("distance").with_near_vector(nearVector).do())
print(result)

# {'data': {'Get': {'YourClass': [{'_additional': {'distance': 0.0750525}, 'frase': "I'm an apple!"}, {'_additional': {'distance': 0.84850264}, 'frase': 'Hello from teh moon!'}]}}}

# Distancia 0 es idéntica. Distancia 1 es opuesta
# La frase "I'm an apple!" es casi idéntica (0.07 distancia) 
# La frase "Hello from teh moon!" está muy alejada (0.84)

# HEMOS CAMBIADO EL MODELO POR LO QUE SALEN RESULTADOS SIMILARES Y COHERENTES PERO NO IGUALES

