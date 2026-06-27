import json 
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim 
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrive(query:str):
    with open("data/memory.json","r",encoding = "utf-8") as file:
        memories = json.load(file)
    print(f"loaded {len(memories)} memories") 

    top_k = 3

    documents = []
    for memory in memories:
        text = (memory["title"]+" "+ memory["overview"])
        documents.append(text)

    memory_embeddings = model.encode(documents)
    print(f"Generated {len(memory_embeddings)} embeddings")


    qurey_embedding = model.encode(query)

    scores  = []

    for i , embedding in enumerate(memory_embeddings):

        similarity = cos_sim(embedding,qurey_embedding)

        scores.append((i, similarity.item()))

    scores.sort(key = lambda x: x[1], reverse = True)

    best_matches = scores[:top_k]
    rag = ''
    print("top_k matches are")

    for i, score in best_matches:
        rag += memories[i]['title']

    return rag