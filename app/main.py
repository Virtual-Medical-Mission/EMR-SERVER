from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, NoSuchColumnError
from typing import List, Dict, Any

# Import database engine and DB_NAME for connection management and display
from .database import engine, DB_NAME

app = FastAPI()

# --- API Endpoints ---

@app.get("/")
def read_root():
    """Confirms API is operational."""
    return {"msg": "EMR API is live"}

@app.get("/test-db")
def test_db_connection():
    """Validates PostgreSQL database connectivity."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT NOW()"))
            current_time = result.scalar()
            return {"status": "success", "db_time": str(current_time)}
    except OperationalError as e:
        return {"status": "error", "message": f"DB connection failed: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred during DB test: {e}"}


@app.get("/patients/{patient_id}")
def get_patient_by_id(patient_id: int):
    """
    Searches for and returns a patient's data by their ID.
    """
    try:
        with engine.connect() as connection:
            # Construct a SQL query to select all patient data by ID
            query = text("SELECT * FROM patients WHERE id = :patient_id")
            result = connection.execute(query, {"patient_id": patient_id})
            patient = result.fetchone()

            if patient is None:
                raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")

            # Convert the result to a dictionary for a clean JSON response
            return dict(patient)

    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"DB connection failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


@app.get("/appointments/{patient_id}")
def get_appointments_by_patient_id(patient_id: int):
    """
    Retrieves all appointments for a given patient ID.
    """
    try:
        with engine.connect() as connection:
            # Query for appointments where the patient_id column matches the input
            query = text("SELECT * FROM appointments WHERE patient_id = :patient_id")
            result = connection.execute(query, {"patient_id": patient_id})
            
            appointments = [dict(row) for row in result]
            
            if not appointments:
                raise HTTPException(status_code=404, detail=f"No appointments found for patient ID {patient_id}.")
            
            return {"patient_id": patient_id, "appointments": appointments}
            
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"DB connection failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


@app.get("/medicine/{medicine_id}")
def get_medicine_by_id(medicine_id: int):
    """
    Fetches details for a specific medicine by its ID.
    """
    try:
        with engine.connect() as connection:
            # Query the medicine table by its primary key
            query = text("SELECT * FROM medicine WHERE id = :medicine_id")
            result = connection.execute(query, {"medicine_id": medicine_id})
            medicine = result.fetchone()

            if medicine is None:
                raise HTTPException(status_code=404, detail=f"Medicine with ID {medicine_id} not found.")

            return dict(medicine)

    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"DB connection failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")