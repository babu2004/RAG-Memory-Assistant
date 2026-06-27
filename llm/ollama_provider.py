from ollama import chat
from .provider import LLMProvider

class OllamaProvider(LLMProvider):
    
    def __init__(self,model = "qwen2.5-coder:3b"):
        self.model = model

    def generate(self, messages):

        response = chat(
            model = self.model,
            messages=messages
        )
        return response["message"]["content"]