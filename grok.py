import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ.get("XAI_API_KEY"), 
    base_url="https://x.ai"
)

try:
    response = client.chat.completions.create(
        model="grok-4.3",  
        messages=[
            {"role": "user", "content": "RAG environment check passing!"}
        ]
    )
    print(response.choices.message.content)
except Exception as e:
    print(f"Error processing model execution: {e}")
