from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables (path fallback to find .env in project root if needed)
load_dotenv(override=True)

from pathlib import Path
env_path = Path(__file__).resolve().parents[4] / '.env'
load_dotenv(dotenv_path=env_path)

class PerplexityProvider:
    @staticmethod
    def generate(prompt: str):
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment variables")
        api_key = api_key.strip()
            
        client = OpenAI(
            api_key=api_key, 
            base_url="https://api.perplexity.ai"
        )

        print(f"DEBUG: base_url={client.base_url}")
        print(f"DEBUG: api_key={api_key[:5]}...")
        try:
            response = client.chat.completions.create(
                model="sonar",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"DEBUG: Error details: {e}")
            raise e

if __name__ == "__main__":
    try:
        print(PerplexityProvider.generate("Hello, how are you?"))
    except Exception as e:
        pass
        