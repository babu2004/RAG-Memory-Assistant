import json
from sentence_transformers.util import cos_sim
import embedder

def retrieve(query: str, top_k=3):
  
    embedding_path =  (embedder.current_dir / "..data/embeddings.json").resolve()

    with open(embedding_path, 'r', encoding='utf-8') as file:
        embeddings_database = json.load(file)

  
    query_embedding = embedder.model.encode(query)

    scores = []


    for item in embeddings_database:
      
        doc_vector = item['embedding'] 
        
     
        similarity = cos_sim(query_embedding, doc_vector)
        
 
        scores.append((item['index'], similarity.item()))
    

    scores.sort(key=lambda x: x[1], reverse=True)


    top_matches = scores[:top_k]

    print(f"Top {top_k} matches for '{query}':\n")

  
    for idx, score in top_matches:
   
        matched_text = embeddings_database[idx]['embedding']
        print(f"Match Index: {idx} (Score: {score:.4f})")
        print(f"Text: {matched_text}\n" + "-"*40)

retrieve("can i join the course", 3)
