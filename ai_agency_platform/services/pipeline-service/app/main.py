from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.graph import app_graph
from langchain_core.messages import HumanMessage

app = FastAPI(title="AI Agency Pipeline Service")

class AgencyRequest(BaseModel):
    prompt: str

@app.post("/run-agency")
async def run_agency(request: AgencyRequest):
    try:
        initial_state = {"messages": [HumanMessage(content=request.prompt)]}
        result = app_graph.invoke(initial_state)
        # Extract the final output (messages, artifacts)
        # For simplicity, returning the messages
        messages = [m.content for m in result['messages']]
        return {
            "status": "success", 
            "messages": messages,
            "artifacts": result.get("artifacts", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
