from pathlib import Path
from sentence_transformers import SentenceTransformer
from ingestion.loaders import load_document
from ingestion.chunker import chunk_text
import chromadb

db_path = Path("chroma_db").resolve()

client = chromadb.PersistentClient(path=str(db_path))
current_dir = Path(__file__).resolve().parent
collection = client.get_or_create_collection("general")
model = SentenceTransformer(
    str(current_dir.parent / "my_local_model")
)


def ingest_document(file_path: str, collection):

    text = load_document(file_path)

    chunks = chunk_text(
        text,
        chunk_size=200,
        chunk_overlap=15
    )

    filename = Path(file_path).stem

    ids = [
        f"{filename}_chunk_{i}"
        for i in range(len(chunks))
    ]

    embeddings = model.encode(chunks)

    metadata = [
        {
            "source": filename,
            "chunk": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadata
    )

    return {
        "filename": filename,
        "chunks": len(chunks)
    }