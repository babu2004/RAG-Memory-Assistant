import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


# --------------------------------------------------
# Paths
# --------------------------------------------------

current_dir = Path(__file__).resolve().parent

embeddings_path = (current_dir / "../data/embeddings.json").resolve()


# --------------------------------------------------
# Load Embedding Model
# --------------------------------------------------

model = SentenceTransformer(
    str(current_dir.parent / "my_local_model")
)


# --------------------------------------------------
# Load Stored Embeddings
# --------------------------------------------------

with open(embeddings_path, "r", encoding="utf-8") as file:

    embedding_data = json.load(file)


# Convert list back to vectors

document_embeddings = [
    item["embedding"]
    for item in embedding_data
]


# --------------------------------------------------
# Retrieve Function
# --------------------------------------------------

def retrieve(query, top_k=3):

    query_embedding = model.encode(query)

    scores = []

    for item in embedding_data:

        similarity = cos_sim(
            query_embedding,
            item["embedding"]
        ).item()

        scores.append(
            {
                "id": item["id"],
                "score": similarity
            }
        )

    scores.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scores[:top_k]