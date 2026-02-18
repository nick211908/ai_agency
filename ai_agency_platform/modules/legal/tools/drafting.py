from typing import Dict, Optional

class LegalDrafter:
    """
    Handles the drafting of legal documents using structured prompts.
    """

    def draft_document(self, doc_type: str, context: Dict) -> str:
        """
        Generates a draft document based on type and context.
        """
        print(f"[LegalDrafter] Drafting {doc_type} with provided context.")
        
        # In a real implementation, this would construct a prompt and call the LLM.
        # For MVP/Simulation, we return a template based on the type.
        
        draft = f"LEGAL DOCUMENT: {doc_type.upper()}\n\n"
        draft += "PARTIES:\n[Party Name 1] and [Party Name 2]\n\n"
        
        if "summary" in context:
            draft += f"BACKGROUND:\n{context['summary']}\n\n"
            
        draft += "TERMS AND CONDITIONS:\n"
        draft += "1. Confidentiality: Both parties agree to keep information confidential.\n"
        draft += "2. Jurisdiction: This agreement is governed by the laws of [State].\n"
        draft += "3. Termination: This agreement may be terminated with 30 days notice.\n"
        
        if doc_type.lower() == "nda":
            draft += "4. Non-Disclosure: The receiving party shall not disclose...\n"
        elif doc_type.lower() == "service agreement":
            draft += "4. Services: The provider agrees to deliver the following services...\n"
            
        draft += "\n[Signature Block]\n"
        
        return draft
