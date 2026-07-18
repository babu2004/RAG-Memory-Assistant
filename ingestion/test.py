
# #testing the loader_text from loaders.py
# from loaders import load_document

# text = load_document("/workspaces/RAG-Memory-Assistant/data/rag.pdf")

# print(text)

""" ========================================================== """

# #testing the chunker.py

# from chunker import chunk_text

# text = """
# Artificial Intelligence is changing the world.

# Large Language Models are becoming increasingly powerful.

# Retrieval-Augmented Generation improves factual accuracy.

# Vector databases store embeddings.

# ChromaDB is an open-source vector database.

# Sentence Transformers create embeddings.
# """


# chunks = chunk_text(text,chunk_size=100,chunk_overlap=20)


# for chunk in chunks:
#     print(chunk)
#     print("-"*40)


"""==========================================="""

# testing ingest.py

from ingest import ingest_document

ingest_document("/workspaces/RAG-Memory-Assistant/data/rag.pdf")