from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import create_db_and_tables
from api import router

# Create FastAPI app
app = FastAPI(
    title="Knowledge Base Backend (Task 2)",
    description="Backend for storing tasks, lessons, and user memory",
    version="1.0.0",
    docs_url="/api/docs",        # Swagger UI
    redoc_url="/api/redoc",      # ReDoc
    openapi_url="/api/openapi.json"
)

# Enable CORS (important for frontend integration later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
create_db_and_tables()

# Include API routes
app.include_router(router, prefix="/api", tags=["knowledge-base"])


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Task 2 Backend 🚀",
        "swagger": "http://127.0.0.1:8000/api/docs",
        "redoc": "http://127.0.0.1:8000/api/redoc"
    }