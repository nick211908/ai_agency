from typing import Dict

class Copywriter:
    """
    Generates marketing copy based on a visual concept or topic.
    """

    def generate_copy(self, topic: str, context: str = "") -> str:
        """
        Generates a caption or ad copy.
        """
        print(f"[Copywriter] Generating copy for: {topic}")
        
        # Mock response
        return f"Transform your {topic} with our premium solution. {context} Experience excellence today! #Innovation #Design"
