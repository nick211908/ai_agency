from typing import TypedDict, Annotated, List, Dict, Any
import operator
from langchain_core.messages import BaseMessage

class LegalAgentState(TypedDict):
    """
    Represents the state of the Legal Agency workflow.
    """
    # Immutable user request
    input: Dict[str, Any]
    
    # Retrieved knowledge (RAG output)
    context: Dict[str, Any]
    
    # Intermediate step outputs (Drafts, Analysis reports)
    intermediate: Dict[str, Any]
    
    # Final deliverable
    output: Dict[str, Any]
    
    # Evaluation scores
    metrics: Dict[str, float]
    
    # Audit trail
    history: List[Dict[str, Any]]
    
    # LangGraph requirements
    messages: Annotated[List[BaseMessage], operator.add]
    next_node: str
