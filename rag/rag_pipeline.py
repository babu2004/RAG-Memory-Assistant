import sys
from pathlib import Path



#to run this file we need to set system path
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from retriever import reterive
from llm.config import provider

def answer_question(query):

    results = reterive(query=query,top_k=3)

    context_parts = []

    for result in results:

        context_parts.append(
            f""" 

                Source: {result['metadata']['source']}
            {result['document']}
            """
        )

    context = "\n --- \n".join(context_parts)

    prompt = f"""
    You are a Retrieval-Augmented Generation.

    Answer the user's question ONLY using the context below.

    If the answer is not contained in the context,
    say:

    "I don't have enough information."

    Context:

    {context}

    User Question:

    {query}
    """
    messages_array = [
{"role": "user", "content": prompt}
]
    response = provider.generate(messages_array)

    return response

