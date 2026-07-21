class DocumentRegistry:

    def __init__(self,collection):

        self.collection = collection
        self.sources = []
        self.refresh()

    def refresh(self):
        # Reloading document names from ChromaDB.

        results = self.collection.get(include=["metadatas"])

        metadatas = results.get("metadatas",[])

        self.sources = sorted({
            metadata["source"]

            for metadata in metadatas
            if metadata and "source" in metadata

        })
    def get_sources(self):
        return self.sources