import sys
import os
import asyncio
from langchain_core.messages import HumanMessage

# Add the pipeline service to path
sys.path.append(os.path.join(os.getcwd(), "services", "pipeline-service"))
sys.path.append(os.path.join(os.getcwd())) # For modules

from app.workflows.legal_agency.graph import legal_graph

async def verify_legal_workflow():
    print("Starting Legal Agency Workflow Verification...")
    
    prompt = "Draft a Service Agreement for a software consulting project."
    
    initial_state = {
        "messages": [HumanMessage(content=prompt)],
        "history": []
    }
    
    try:
        # Invoke the graph with higher recursion limit for loops
        result = await legal_graph.ainvoke(initial_state, {"recursion_limit": 50})
        
        print("\n--- Workflow Execution Complete ---")
        
        # Verify State Population
        assert "context" in result, "Context missing"
        assert "intermediate" in result, "Intermediate outputs missing"
        assert "output" in result, "Final output missing"
        assert "metrics" in result, "Metrics missing"
        assert "history" in result, "Audit history missing"
        
        print("\n[Audit Trail]")
        for entry in result['history']:
            print(f"- {entry['step']} @ {entry['timestamp']}")
            
        print("\n[Metrics]")
        print(result['metrics'])
        
        print("\n[Final Document Snippet]")
        doc = result['output'].get('document', '')
        print(doc[:200] + "...")
        
        # Save to file for user inspection
        output_path = "generated_service_agreement.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(doc)
        print(f"\n[Info] Full document saved to: {output_path}")
        
        if "CITATIONS" in doc:
            print("\n[Success] Citations found in document.")
        else:
            print("\n[Warning] Citations NOT found in document.")
            
        print("\nVerification Passed!")
        
    except Exception as e:
        print(f"\n[Error] Verification Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_legal_workflow())
