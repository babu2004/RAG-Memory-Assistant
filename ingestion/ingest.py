from pathlib import Path 
from sentence_transformers import SentenceTransformer
from loaders import load_text
from chunker import chunk_text
import chromadb 

current_dir = Path(__file__).resolve().parent

db_path = Path(current_dir.parent/"chroma_db").resolve()

model = SentenceTransformer(str(current_dir.parent/"my_local_model"))

client = chromadb.PersistentClient(
    path = str(db_path)
)

collection = client.get_collection("faq")

def ingest_document(file_path:str):

    text = load_text(file_path)

    chunks = chunk_text(text,chunk_size=200,overlap=15)

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

    print(f"ingested {len(chunks)} chunks from {filename}")

