from sentence_transformers import CrossEncoder

class Reranker:

    def __init__(self):
        
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query, chunks, top_k=3):

        pairs = [
            (query,chunk["document"])
            for chunk in chunks
        ]

        scores = self.model.predict(pairs)

        ranked_chunk = chunks.copy()


        for chunk, score in zip(ranked_chunk,scores):
            chunk["rerank_score"] = float(score)
        
        ranked_chunk.sort(key = lambda chunk:chunk["rerank_score"], reverse = True)

        return ranked_chunk[:top_k]