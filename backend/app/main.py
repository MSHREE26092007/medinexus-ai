"""MediNexus AI — FastAPI entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import patients, dashboard

# Create tables on startup (hackathon: no Alembic needed)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MediNexus AI",
    description="Autonomous Offline Clinical Intelligence Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(dashboard.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "medinexus-ai"}
