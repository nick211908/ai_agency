import sys
import os

# Add the service root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.graph import app_graph
from langchain_core.messages import HumanMessage

def test_design_workflow():
    print("Testing Design Agency Workflow...")
    prompt = "Create a social media campaign for a new coffee brand."
    initial_state = {"messages": [HumanMessage(content=prompt)]}
    
    try:
        result = app_graph.invoke(initial_state)
        print("\nWorkflow Execution Successful!")
        print("-" * 30)
        for msg in result['messages']:
            print(f"[{msg.name}]: {msg.content[:100]}...") # Truncate for readability
        print("-" * 30)
        
        # Verify we reached the end and have artifacts (optional check based on mocked logic)
        # Our mock nodes return artifacts in the state
        if 'artifacts' in result:
             print(f"Artifacts generated: {result['artifacts'].keys()}")

    except Exception as e:
        print(f"Workflow Execution Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_design_workflow()
