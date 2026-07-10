
# #testing the loader_text
# from chunker import load_text

# text = load_text("/workspaces/RAG-Memory-Assistant/data/test.txt")

# print(text)

from chunker import chunk_text

text = """
Artificial Intelligence is changing the world.

Large Language Models are becoming increasingly powerful.

Retrieval-Augmented Generation improves factual accuracy.

Vector databases store embeddings.

ChromaDB is an open-source vector database.

Sentence Transformers create embeddings.
"""


chunks = chunk_text(text,chunk_size=50,overlap=10)


for i, chunk in enumerate(chunks):

    print("="*40)

    print(f"chunk:{i+1}")

    print("="*40)
    print(chunk)