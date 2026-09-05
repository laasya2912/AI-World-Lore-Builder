from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
import models

from routes.world import router as world_router
from routes.lore import router as lore_router
from routes.consistency import router as consistency_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="AI World Lore Builder API",
    description="Backend API for generating and managing interconnected fictional worlds",
    version="1.0.0"
)


# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routes
app.include_router(world_router)
app.include_router(lore_router)
app.include_router(consistency_router)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "AI World Lore Builder Backend is running!"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }