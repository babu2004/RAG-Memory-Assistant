import json 
from pathlib import Path
from sentence_transformers import SentenceTransformer

# 1. Safely locate your local model relative to this file
current_dir = Path(__file__).resolve().parent
model = SentenceTransformer(str(current_dir.parent / "my_local_model"))

def build_embeddings():
    # 2. Fix the file paths so they don't break based on terminal folder
    faq_path = (current_dir / "../data/faq.json").resolve()
    embeddings_path = (current_dir / "../data/embeddings.json").resolve()

    with open(faq_path, "r", encoding="utf-8") as file:
        memorys = json.load(file)

    documents = []
    for memory in memorys:
        text = (memory['course'] + " " + memory['question'])
        documents.append(text)

    
    memory_embeddings = model.encode(documents)

    structured_data = []

    for memory, embedding in zip(memorys, memory_embeddings):

        structured_data.append(
            {
                "id": memory["id"],
                "course": memory["course"],
                "embedding": embedding.tolist()
            }
        )
    
    with open(embeddings_path, 'w', encoding='utf-8') as file:
        json.dump(structured_data, file, indent=4)
        
    print(f"Successfully processed {len(documents)} items and saved embeddings!")

build_embeddings()

