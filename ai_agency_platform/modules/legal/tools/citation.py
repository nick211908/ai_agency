from typing import List, Dict

class CitationEngine:
    """
    Ensures grounding by attaching relevant citations to generated content.
    """

    def attach_citations(self, content: str, sources: List[Dict]) -> str:
        """
        Appends a list of sources to the document. 
        In production, this would use semantic matching to inline citations.
        """
        print("[CitationEngine] Attaching sources to document.")
        
        citated_content = content + "\n\n--- CITATIONS ---\n"
        
        if not sources:
            citated_content += "No sources cited."
            return citated_content
            
        for idx, source in enumerate(sources, 1):
            if "citation" in source:
                citation = source["citation"]
                name = source.get("case_name", "Unknown Case")
                citated_content += f"[{idx}] {name}, {citation}\n"
            elif "statute_name" in source:
                name = source["statute_name"]
                citated_content += f"[{idx}] {name}\n"
            else:
                citated_content += f"[{idx}] Unknown Source\n"
                
        return citated_content
