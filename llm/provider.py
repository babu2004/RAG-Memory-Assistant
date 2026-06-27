class LLMProvider:
    def generate(self,messages):
        raise NotImplementedError(
            "provider must implement generate()"
        )