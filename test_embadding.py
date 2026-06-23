from  sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

sentence1 = "openAI created ChatGPT"
sentence2 = "coconut chutney is tasty"
sentence3 = "how to make dosa"



embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)
embedding3 = model.encode(sentence3)

similarity_1_2 = cos_sim(embedding1,embedding2)
similarity_2_3 = cos_sim(embedding2,embedding3)
similarity_1_3 = cos_sim(embedding1,embedding3)

print(
    "chatgpt ↔ coconut:",
    similarity_1_2.item()
)

print(
    "chatgpt ↔ dosa:",
    similarity_1_3.item()
)

print(
    "coconut ↔ dosa:",
    similarity_2_3.item()
)