from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.graph import app_graph
from langchain_core.messages import HumanMessage

app = FastAPI(title="AI Agency Pipeline Service")

# Allow browser-based frontends (local dev and configurable origins)
# so responses can be consumed and rendered by UI clients.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgencyRequest(BaseModel):
    prompt: str


@app.post("/run-agency")
async def run_agency(request: AgencyRequest):
    try:
        initial_state = {"messages": [HumanMessage(content=request.prompt)]}
        result = app_graph.invoke(initial_state)

        message_objects = result.get("messages", [])
        messages = [m.content for m in message_objects]
        timeline = [
            {"role": getattr(m, "name", "assistant"), "content": m.content}
            for m in message_objects
        ]
        final_message = messages[-1] if messages else ""
        artifacts = result.get("artifacts", {})

        # Keep backward compatibility with multiple frontend response shapes.
        return {
            "status": "success",
            "messages": messages,
            "artifacts": artifacts,
            # common frontend expectations
            "response": final_message,
            "output": {
                "response": final_message,
                "messages": messages,
                "timeline": timeline,
                "artifacts": artifacts,
            },
            "data": {
                "response": final_message,
                "messages": messages,
                "timeline": timeline,
                "artifacts": artifacts,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok"}
