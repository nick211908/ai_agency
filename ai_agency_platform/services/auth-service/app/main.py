from fastapi import FastAPI
from app.api.endpoints import auth
from app.core.config import settings
from app.db.base_class import Base
from app.db.session import engine

# Create tables
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Auth Service"}
