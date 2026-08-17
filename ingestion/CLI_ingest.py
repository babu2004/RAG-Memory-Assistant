import chromadb
from pathlib import Path

from ingestion.ingest import ingest_document
from rag.document_registry import DocumentRegistry

db_path = Path("chroma_db").resolve()

client = chromadb.PersistentClient(path=str(db_path))

collection = client.get_or_create_collection("general")

result = ingest_document(
    "data/rag.pdf",
    collection 
)

registry = DocumentRegistry(collection)
registry.refresh()

print(
    f"Ingested {result['chunks']} chunks from {result['filename']}"
)