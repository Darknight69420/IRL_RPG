from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
import app.models  # Ensure all SQLAlchemy models are registered
from app.services.seed_data import seed_database
from app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and seed data if not present
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield
    # Shutdown: Clean up resources if needed

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS configuration for Frontend (Person 2)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "LIFE RPG / LIFEDEX Game Engine API",
        "version": "1.0.0"
    }

@app.get("/", tags=["System"])
def root():
    return {
        "message": "Welcome to LIFE RPG / LIFEDEX API. Real-life habits develop living Anima companions.",
        "documentation": "/docs"
    }

app.include_router(api_router, prefix=settings.API_V1_STR)
