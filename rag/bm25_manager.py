from rank_bm25 import BM25Okapi


class BM25Manager:
    
    def __init__(self,collection):

        self.collection = collection
        
        self.id = []
        self.documents = []
        self.metadatas = []

        self.bm25 = None

        self.refresh()

    def refresh(self):

        results = self.collection.get(
            include = ["documents","metadatas"]
        )

        self.documents = results["documents"]
        self.ids = results["ids"]
        self.metadatas = results["metadatas"]

        tokenized = [

            doc.lower().split()
            for doc in self.documents
        ]

        self.bm25 = BM25Okapi(tokenized)


    def search(self, query, top_k=5):

        query_tokens = query.lower().split()
        scores = self.bm25.get_scores(query_tokens)

        top_indeces = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse = True
        )[:top_k]
        
        output = [
            {
                "ids":i,
                "documents":self.documents[i],
                "metadatas":self.metadatas[i]["source"],
                "scores":scores[i]
            }
            for i in top_indeces
        ]

        return output
        


        
