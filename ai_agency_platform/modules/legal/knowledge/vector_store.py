import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict

class VectorStore:
    """
    Manages embedding generation and retrieval using ChromaDB.
    """
    
    def __init__(self, collection_name: str = "legal_knowledge"):
        self.client = chromadb.Client() # In-memory for MVP
        # Use a lightweight, open-source embedding model
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def add_documents(self, documents: List[str], metadatas: List[Dict] = None):
        """
        Adds documents to the vector store.
        """
        if not documents:
            return
            
        ids = [f"doc_{i}_{hash(doc)}" for i, doc in enumerate(documents)]
        
        if metadatas is None:
            metadatas = [{"source": "unknown"} for _ in documents]
            
        print(f"[VectorStore] Adding {len(documents)} chunks to collection.")
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, n_results: int = 3) -> List[Dict]:
        """
        Retrieves relevant documents for a query.
        """
        print(f"[VectorStore] Querying: {query_text}")
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        # Flatten results structure
        flattened = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i] if results['metadatas'] else {}
                flattened.append({
                    "text": doc,
                    "metadata": meta,
                    "distance": results['distances'][0][i] if 'distances' in results and results['distances'] else 0
                })
                
        return flattened
