import json 
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim 
model = SentenceTransformer("all-MiniLM-L6-v2")

with open("memory.json","r",encoding = "utf-8") as file:
    memories = json.load(file)
print(f"loaded {len(memories)} memories") 

documents = []
for memory in memories:
    text = (memory["title"]+" "+ memory["overview"])
    documents.append(text)

memory_embeddings = model.encode(documents)
print(f"Generated {len(memory_embeddings)} embeddings")


query = "robots are scary"

qurey_embedding = model.encode(query)

scores  = []

for i , embedding in enumerate(memory_embeddings):

    similarity = cos_sim(embedding,qurey_embedding)

    scores.append((i, similarity.item()))

scores.sort(key = lambda x: x[1], reverse = True)

best_index = scores[0][0]
best_memory = memories[best_index]
print("\nBest_match:\n")
print(best_memory["title"])

print()

print(best_memory["overview"])