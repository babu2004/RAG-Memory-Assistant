import json 
from pathlib import Path
import sys

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from retriever import retrieve
from llm.config import provider

faq_path = (current_dir / "../data/faq.json").resolve()

with open(faq_path,"r",encoding = "utf-8") as file:
    faq_documents = json.load(file)


faq_lookup = {
    faq['id']:faq
    for faq in faq_documents
}

def answer_question(query):

    results = retrieve(query=query,top_k=3)

    context = ""

    for result in results:

        faq = faq_lookup[result["id"]]

        context += f"""
        
        Course:
        {faq["course"]}

        Question:
        {faq["question"]}

        Answer:
        {faq["answer"]}


        --------------------------------------------------------------
        """

        prompt = f"""
        You are a teaching assistant for DataTalksClub.

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

