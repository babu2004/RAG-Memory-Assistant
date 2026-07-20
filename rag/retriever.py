from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from source_detection import detect_source
from document_registry import DocumentRegistry

current_dir = Path(__file__).resolve().parent

db_path = (current_dir.parent / "chroma_db").resolve()

model = SentenceTransformer(str(current_dir.parent/"my_local_model"))

client = chromadb.PersistentClient(
    path = str(db_path)
)

collection = client.get_collection(
    "general"
)
registry = DocumentRegistry(collection)


def reterive(query,top_k):

    source = detect_source(query, registry)

    query_embedding = model.encode(query).tolist()
    
    if source:
            results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where = {"source":source}
    )


    else:
    
        results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrived = []

    for doc_id, document, metadata, distance in zip(results["ids"][0],results["documents"][0],results["metadatas"][0],results["distances"][0]):

        retrived.append(
            {
                "id":doc_id,
                "document":document,
                "metadata":metadata,
                "score":1 - distance
            }
        )

    return retrived