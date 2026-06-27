from sentence_transformers import SentenceTransformer
from sematic_memory import retrive
from llm.config import provider
print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model loaded successfully!") 

question = input("ask the rag: ")

context =  retrive(question)

rag_prompt = f'''
    You are a helpful, secure, and accurate assistant. Your task is to answer the user's question using ONLY the provided context blocks below.

[CONTEXT]
{context}
[END OF CONTEXT]

Strict Guidelines:
1. Grounding: Rely strictly on the clear facts directly mentioned in the context. Do not assume, extrapolate, or bring in outside knowledge.
2. Unanswerable Questions: If the context does not contain the exact answer to the question, state clearly: "I am sorry, but the provided documentation does not contain enough information to answer your question."
3. No Speculation: Never say things like "Based on my knowledge..." or "The text implies...". If it is not explicitly written, it does not exist.

User Question: {question}
Answer:

'''


answer = provider.generate(
    [
        {
            "role":"user",
            "content":rag_prompt
        }
    ]
)

print(answer)