from fastapi import FastAPI
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
    """Validates PostgreSQL database connectivity and returns current DB time."""
    return test_db_connection()

@app.get("/map-db")
def map_db():
    """
    Returns the database schema: tables, columns, primary keys, and foreign keys.
    """
    return map_database_schema()

@app.get("/check-storage")
def check_storage():
    """Checks if the lightsail storage bucket is accessible."""
    status = check_bucket_access()
    return {
        "bucket": bucket_name,
        "status": "accessible" if status else "unreachable"
    }

@app.get("/map-storage")
def map_storage():
    """
    Lists all objects in the bucket. Optionally, filter by prefix.
    Returns a list of object keys.
    """
    return map_bucket_contents()
