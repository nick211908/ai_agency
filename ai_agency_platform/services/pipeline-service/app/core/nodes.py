from langchain_core.messages import HumanMessage, AIMessage
from app.core.state import AgentState
import json

import httpx
import os

# LLM Service URL (default to localhost for dev)
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://localhost:8000/generate")

def call_llm(prompt: str, role: str) -> str:
    """Calls the LLM service to generate a response."""
    try:
        # Construct the full prompt with role context
        full_prompt = f"Role: {role}. Task: {prompt}"
        response = httpx.get(LLM_SERVICE_URL, params={"prompt": full_prompt}, timeout=30.0)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"Warning: LLM Service call failed ({e}). Using mock response.")
        # Fallback to mock responses
        if role == "Project Manager":
            return json.dumps({
                "plan": [
                    "1. Analyze target audience for coffee brand",
                    "2. Create visual concept for launch post",
                    "3. Draft compelling copy for product features"
                ],
                "next_step": "designer"
            })
        elif role == "Designer":
            return "Image Prompt: A steaming cup of artisanal coffee on a rustic wooden table, morning sunlight streaming through a window, 4k, photorealistic."
        elif role == "Copywriter":
            return "Caption: Start your day with the perfect brew. ☕✨ #CoffeeLover #MorningVibes"
        elif role == "Creative Director":
            return "Feedback: The image prompt is good, but let's make the caption punchier. APPROVED."
        return "Error: Unknown role"

def project_manager_node(state: AgentState):
    """Breaks down the user request into tasks."""
    user_input = state['messages'][-1].content
    response = call_llm(f"As a Project Manager, break down this request: {user_input}", "Project Manager")
    return {
        "messages": [AIMessage(content=response, name="Project Manager")],
        "next_node": "designer",
        # parsing the mocked json response 
        "current_task": "Design Phase" 
    }

def designer_node(state: AgentState):
    """Generates design concepts."""
    response = call_llm("Generate a visual concept.", "Designer")
    return {
        "messages": [AIMessage(content=response, name="Designer")],
        "next_node": "copywriter",
        "artifacts": {"design_concept": response}
    }

def copywriter_node(state: AgentState):
    """Writes copy based on design."""
    response = call_llm("Write copy for the design.", "Copywriter")
    return {
        "messages": [AIMessage(content=response, name="Copywriter")],
        "next_node": "creative_director",
        "artifacts": {"copy_draft": response}
    }

def creative_director_node(state: AgentState):
    """Reviews the work."""
    response = call_llm("Review the work.", "Creative Director")
    return {
        "messages": [AIMessage(content=response, name="Creative Director")],
        "next_node": "end", # End of workflow
        "artifacts": {"review_feedback": response}
    }
