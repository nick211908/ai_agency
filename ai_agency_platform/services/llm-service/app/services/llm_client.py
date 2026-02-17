import sys
import os

# Add the parent directory of 'app' to sys.path so 'app' module can be found when run directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.providers.perplexity_provider import PerplexityProvider

class LLMClient:
    def __init__(self, provider: str = "perplexity"):
        self.provider = provider

    def generate(self, prompt: str) -> str:
        if self.provider == "perplexity":
            return PerplexityProvider.generate(prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

if __name__ == "__main__":
    client = LLMClient()
    print(client.generate("Hello from LLMClient!"))
