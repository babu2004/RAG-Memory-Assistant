from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb


current_dir = Path(__file__).resolve().parent

db_path = (current_dir.parent / "chroma_db").resolve()

model = SentenceTransformer(str(current_dir.parent/"my_local_model"))

client = chromadb.PersistentClient(
    path = str(db_path)
)

collection = client.get_collection(
    "faq"
)

def reterive(query,top_k):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrived = []

    for doc_id, distance in zip(results["ids"][0],results["distances"][0]):

        retrived.append(
            {
                "id":doc_id,
                "score":1 - distance
            }
        )

    return retrived