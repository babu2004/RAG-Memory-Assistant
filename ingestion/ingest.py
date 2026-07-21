from pathlib import Path 
from sentence_transformers import SentenceTransformer
from .loaders import load_document
from .chunker import chunk_text
import chromadb 
from rag.document_registry import DocumentRegistry





current_dir = Path(__file__).resolve().parent

db_path = Path(current_dir.parent/"chroma_db").resolve()

model = SentenceTransformer(str(current_dir.parent/"my_local_model"))

client = chromadb.PersistentClient(
    path = str(db_path)
)

collection = client.get_or_create_collection(name ="general")
registry = DocumentRegistry(collection)
def ingest_document(file_path:str):

    text = load_document(file_path)

    chunks = chunk_text(text,chunk_size=200,chunk_overlap=15)

    filename = Path(file_path).stem

    ids = [
        f"{filename}_chunk_{i}"
        for i in range(len(chunks)) 
    ]

    embeddings = model.encode(chunks)

    # creating metadata 

    metadata = []

    for i in range(len(chunks)):

        metadata.append(
            {
                "source":filename,
                "chunk":i
            }
        )

    collection.add(
        ids = ids,
        documents = chunks,
        embeddings = embeddings.tolist(),
        metadatas = metadata
    )
    registry.refresh()

    print(f"ingested {len(chunks)} chunks from {filename}")

