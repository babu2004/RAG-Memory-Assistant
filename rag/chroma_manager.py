import json
from pathlib import Path
import chromadb 
from sentence_transformers import SentenceTransformer


current_dir = Path(__file__).resolve().parent
faq_path = (current_dir / "../data/faq.json").resolve()
db_path = (current_dir.parent / "chroma_db").resolve()

# loading embedder model
model = SentenceTransformer(str (current_dir.parent/"my_local_model"))

# chroma client
client = chromadb.PersistentClient(
    path = str(db_path)
)

# creating collection 
collection = client.get_or_create_collection(
    name = "faq"
)

def build_database():

    with open(faq_path,"r",encoding="utf-8") as file:
        faq_documents = json.load(file)


    try:
        client.delete_collection("faq")
    except:
        pass
    
    collection = client.create_collection("faq")

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for faq in faq_documents:

        text = (
            faq["course"]
            + " " +
            faq["question"]
        )

        embedding = model.encode(text)

        ids.append(str(faq["id"]))

        documents.append(text)

        embeddings.append(embedding.tolist())

        metadatas.append(
            {
                  "course":faq["course"],
                  "section":faq["section"]  
            }
        )

        collection.add(
            ids = ids,
            documents = documents,
            embeddings = embeddings,
            metadatas = metadatas
        )

    print(f"stored {len(ids)} documents in chromadb")

build_database()