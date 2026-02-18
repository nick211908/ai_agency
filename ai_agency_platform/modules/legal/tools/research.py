import json
from typing import List, Dict
import os
import sys

# Add path to import modules
sys.path.append(os.path.join(os.getcwd(), "..", "..", ".."))

from modules.legal.knowledge.vector_store import VectorStore

class LegalResearcher:
    """
    Conducts legal research using RAG (Retrieval Augmented Generation).
    Connects to the VectorStore to retrieve relevant ingested documents.
    """

    def __init__(self):
        try:
            self.store = VectorStore()
        except:
            print("VectorStore not available, falling back to mock.")
            self.store = None

    def search_case_law(self, query: str) -> List[Dict]:
        """
        Searches for case law in the Vector Store.
        """
        if not self.store:
            return self._mock_case_law(query)
            
        print(f"[LegalResearcher] RAG Search for case law: {query}")
        results = self.store.query(query, n_results=3)
        
        # Format for context
        formatted = []
        for res in results:
            formatted.append({
                "case_name": res['metadata'].get('source', 'Unknown Document'),
                "citation": "Ingested Document",
                "summary": res['text'],
                "relevance_score": 1.0 - res['distance']
            })
        return formatted

    def retrieve_statutes(self, query: str) -> List[Dict]:
        """
        Searches for statutes/rules in the Vector Store.
        """
        if not self.store:
            return self._mock_statutes(query)
            
        print(f"[LegalResearcher] RAG Search for statutes: {query}")
        results = self.store.query(query + " statute rule law", n_results=2)
        
        formatted = []
        for res in results:
            formatted.append({
                "statute_name": res['metadata'].get('source', 'Unknown Statute'),
                "text": res['text'],
                "relevance_score": 1.0 - res['distance']
            })
        return formatted

    def _mock_case_law(self, query):
        return [
            {
                "case_name": "Mock Case v. Test",
                "citation": "123 Mock 456",
                "summary": "This is a mock case summary because VectorStore is unavailable.",
                "relevance_score": 0.0
            }
        ]

    def _mock_statutes(self, query):
        return []

    def summarize_findings(self, findings: List[Dict]) -> str:
        """
        Summarizes the research findings into a coherent context string.
        """
        summary = "Legal Research Summary (from RAG):\n\n"
        for item in findings:
            if "case_name" in item:
                summary += f"- Source: {item['case_name']}\n  Content: {item['summary'][:300]}...\n"
            elif "statute_name" in item:
                summary += f"- Source: {item['statute_name']}\n  Text: {item['text'][:300]}...\n"
        return summary

    def get_structured_context(self, query: str) -> Dict:
        """
        Orchestrates the research process and returns a structured context.
        """
        cases = self.search_case_law(query)
        statutes = self.retrieve_statutes(query)
        findings = cases + statutes
        summary = self.summarize_findings(findings)
        
        return {
            "query": query,
            "cases": cases,
            "statutes": statutes,
            "summary": summary
        }
