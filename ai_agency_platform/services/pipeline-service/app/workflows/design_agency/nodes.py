from langchain_core.messages import AIMessage
from app.workflows.design_agency.state import DesignAgentState
import sys
import os

# Add modules path for imports if not already there
sys.path.append(os.path.join(os.getcwd(), "..", "..", ".."))

from modules.design.tools.image_gen import ImageGenerator
from modules.design.tools.copywriter import Copywriter

def intake_node(state: DesignAgentState):
    """
    Initializes the workflow from user input.
    """
    input_data = state.get('input', {})
    request = input_data.get('request', 'Create a visual concept.')
    
    return {
        "messages": [AIMessage(content=f"Design Request Received: {request}", name="Intake")],
        "artifacts": {},
        "review": {},
        "next_node": "designer"
    }

def designer_node(state: DesignAgentState):
    """
    Generates visual concepts using the ImageGenerator.
    """
    print("[Nodes] Designer Node Executing...")
    input_data = state.get('input', {})
    request = input_data.get('request', 'Create a visual concept.')
    
    gen = ImageGenerator()
    image_result = gen.generate_image(request)
    
    return {
        "messages": [AIMessage(content=f"Generated visual concept: {image_result['url']}", name="Designer")],
        "artifacts": {"image": image_result},
        "next_node": "copywriter"
    }

def copywriter_node(state: DesignAgentState):
    """
    Generates copy based on the design concept.
    """
    print("[Nodes] Copywriter Node Executing...")
    input_data = state.get('input', {})
    artifacts = state.get('artifacts', {})
    
    topic = input_data.get('request', 'product')
    image_context = artifacts.get('image', {}).get('prompt', '')
    
    writer = Copywriter()
    copy_text = writer.generate_copy(topic, context=image_context)
    
    return {
        "messages": [AIMessage(content=f"Drafted copy: {copy_text}", name="Copywriter")],
        "artifacts": {"copy": copy_text},
        "next_node": "review"
    }

def review_node(state: DesignAgentState):
    """
    Simulates a Creative Director review.
    """
    print("[Nodes] Review Node Executing...")
    
    # Mock auto-approval for now
    return {
        "messages": [AIMessage(content="Creative Director: Looks good. Approved.", name="Creative Director")],
        "review": {"status": "approved", "comments": "Good job."},
        "next_node": "end"
    }
