import pathlib import Path 
from sentence_transformers import SentenceTransformer
from loaders import load_text
from chunker import chunk_text
import chromadb 

current_dir = Path(__file__).resolve().parent

db_path = Path(current_dir.parent/"chroma_db").resolve()

model = SentenceTransformer(str(current_dir.parent/"my_local_model"))

client = chroma_db.PersistentClient(
    path = str(db_path)
)

collection = client.get_collection("faq")