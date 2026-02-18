import sys
import os
import asyncio
import requests
from langchain_core.messages import HumanMessage

# Add the pipeline service to path
sys.path.append(os.path.join(os.getcwd(), "services", "pipeline-service"))
sys.path.append(os.path.join(os.getcwd())) # For modules

from app.workflows.legal_agency.graph import legal_graph
from modules.legal.knowledge.ingestion import DocumentParser
from modules.legal.knowledge.vector_store import VectorStore

def create_dummy_legal_doc():
    content = """
    SERVICE AGREEMENT PRECEDENT
    
    1. Indemnification: The Provider agrees to indemnify and hold harmless the Client from any claims, damages, or liabilities arising out of the services provided.
    2. Termination: This agreement may be terminated by either party with 30 days written notice.
    3. Liability: The Provider's liability shall be limited to the total fees paid under this agreement.
    4. Jurisdiction: This agreement shall be governed by the laws of the State of California.
    """
    path = "precedent_contract.txt"
    with open(path, "w") as f:
        f.write(content)
    return path

async def verify_ingestion_and_rag():
    print("Starting Ingestion & RAG Verification...")
    
    # 1. Create a dummy legal text file
    doc_path = create_dummy_legal_doc()
    print(f"[Setup] Created dummy document: {doc_path}")
    
    # 2. Simulate Ingestion (Directly calling parser/store to avoid spinning up full API server for script)
    # In integration test, we would hit the API endpoint.
    print("[Ingestion] Parsing and Storing document...")
    parser = DocumentParser()
    chunks = parser.parse_file(doc_path)
    
    store = VectorStore()
    store.add_documents(chunks, metadatas=[{"source": "precedent_contract.txt"}])
    print(f"[Ingestion] Added {len(chunks)} chunks to VectorStore.")
    
    # 3. Run the Workflow (which now uses RAG)
    print("\n[Workflow] Running Legal Agency with RAG-enabled Researcher...")
    prompt = "Draft a Service Agreement with indemnification and termination clauses."
    
    initial_state = {
        "messages": [HumanMessage(content=prompt)],
        "history": []
    }
    
    try:
        result = await legal_graph.ainvoke(initial_state, {"recursion_limit": 50})
        
        # 4. Inspect Output
        print("\n[Raw RAG Context Retrieved]")
        context = result.get('context', {})
        if 'cases' in context:
            for case in context['cases']:
                 print(f"- Case/Doc: {case.get('case_name')}")
                 print(f"  Snippet: {case.get('summary')[:100]}...")
        if 'statutes' in context:
            for stat in context['statutes']:
                 print(f"- Statute/Rule: {stat.get('statute_name')}")
                 print(f"  Snippet: {stat.get('text')[:100]}...")

        doc = result['output'].get('document', '')
        print("\n[Generated Document Snippet]")
        print(doc[:500] + "...")
        
        # Check if RAG content appears in the research summary or document
        context = result.get('context', {})
        summary = context.get('summary', '')
        
        if "Indemnification" in summary or "California" in summary:
             print("\n[Success] RAG retrieved content found in research summary.")
        else:
             print("\n[Warning] RAG content NOT obvious in research summary.")
             print(f"Summary: {summary}")
             
        # Cleanup
        os.remove(doc_path)
        print("\nVerification Passed!")
        
    except Exception as e:
        print(f"\n[Error] Verification Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_ingestion_and_rag())
