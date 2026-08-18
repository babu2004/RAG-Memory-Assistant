import os
from dotenv import  load_dotenv 
from openai import OpenAI
from .provider import LLMProvider

load_dotenv()


client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("XAI_API_KEY") 
)



class GrokProvider(LLMProvider):
    
    #  New updated model name
    def __init__(self, model="qwen/qwen3.6-27b"): 

        self.model = model

    def generate(self, messages):
        
            response = client.chat.completions.create(
          
            model=self.model, 
            messages=messages,
            temperature=0.7,
            max_completion_tokens=800  
        )
            return response.choices[0].message.content
