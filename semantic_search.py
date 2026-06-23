
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

documents = [

    "OpenAI is an AI research company.",

    "Machine Learning allows computers to learn from data.",

    "Pizza is a popular Italian dish."

]

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

document_embeddings = model.encode(
    documents
)


query = "How do computers learn?"

query_embedding = model.encode(query)

scores = []

for i, document_embedding in enumerate(document_embeddings):

    similarity = cos_sim(
        query_embedding,
        document_embedding
    )

    scores.append(
        (
            documents[i],
            similarity.item()
        )
    )

scores.sort(
    key=lambda x: x[1],
    reverse=True
)

print("\nSemantic Search Results:\n")

for document, score in scores:

    print(
        f"{score:.4f} -> {document}"
    )