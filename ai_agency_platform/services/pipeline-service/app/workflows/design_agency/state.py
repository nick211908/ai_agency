from typing import TypedDict, Annotated, List, Dict, Any
import operator
from langchain_core.messages import BaseMessage

class DesignAgentState(TypedDict):
    """
    Represents the state of the Design Agency workflow.
    """
    # Immutable user request
    input: Dict[str, Any]
    
    # Generated artifacts
    artifacts: Dict[str, Any]
    
    # Feedback / Review status
    review: Dict[str, Any]
    
    # LangGraph requirements
    messages: Annotated[List[BaseMessage], operator.add]
    next_node: str
