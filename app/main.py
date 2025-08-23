from fastapi import FastAPI, HTTPException, status
from sqlalchemy import text, inspect
from sqlalchemy.exc import OperationalError

from .connections.database import test_db_connection, map_database_schema
from .connections.storage import check_bucket_access, bucket_name, map_bucket_contents

from .codein import router as in_memory_router


app = FastAPI(
    title="EMR API",
    description="EMR API with database/storage testing and in-memory demo features.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(in_memory_router)

# --- API Endpoints ---

@app.get("/")
def read_root():
    """Confirms API is operational."""
    return {"message": "EMR-API is live and functional"}

@app.get("/test-db")
def test_db():
    """Validates PostgreSQL database connectivity."""
    try:
        return test_db_connection()
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {e}"
        )

@app.get("/map-db")
def map_db():
    """Returns the database schema."""
    try:
        return map_database_schema()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not map database schema. Is the connection OK? Error: {e}"
        )

@app.get("/check-storage")
def check_storage():
    """Checks if the lightsail storage bucket is accessible."""
    try:
        is_accessible = check_bucket_access()
        return {
            "bucket": bucket_name,
            "status": "accessible" if is_accessible else "unreachable"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Storage check failed: {e}")

@app.get("/map-storage")
def map_storage():
    """Lists all objects in the storage bucket."""
    try:
        return map_bucket_contents()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Could not map storage contents: {e}")
