from fastapi import FastAPI
from sqlalchemy import text, inspect
from sqlalchemy.exc import OperationalError

from .connections.database import engine, DB_NAME
from .connections.storage import check_bucket_access, bucket_name


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
        # Handles database connection failures (e.g., credentials, firewall)
        return {"status": "error", "message": f"DB connection failed: {e}"}
    except Exception as e:
        # Catches other unexpected errors during DB test
        return {"status": "error", "message": f"An unexpected error occurred during DB test: {e}"}

@app.get("/map-db")
def map_database_schema():
    """
    Connects to the database and returns its tables and columns as JSON.
    Useful for inspecting the current database schema.
    """
    db_schema = {"database_name": DB_NAME, "tables": []}
    try:
        inspector = inspect(engine)
        table_names = inspector.get_table_names()

        if not table_names:
            db_schema["message"] = f"No tables found in database '{DB_NAME}'."
            return db_schema

        for table_name in table_names:
            table_info = {"name": table_name, "columns": []}
            columns = inspector.get_columns(table_name)

            for column in columns:
                col_info = {
                    "name": column['name'],
                    "type": str(column['type']), # Convert SQLAlchemy Type to string
                    "nullable": column['nullable'],
                    "primary_key": column['primary_key']
                }
                # Add foreign key information
                fk_info = inspector.get_foreign_keys(table_name, column_name=column['name'])
                if fk_info:
                    # For simplicity, if multiple FKs on one column, take the first.
                    first_fk = fk_info[0]
                    col_info["foreign_key"] = {
                        "referred_table": first_fk['referred_table'],
                        "referred_column": first_fk['referred_columns'][0]
                    }
                table_info["columns"].append(col_info)

            # Add primary key constraint info at table level
            pks = inspector.get_pk_constraint(table_name)
            if pks and pks['constrained_columns']:
                table_info["primary_key_columns"] = pks['constrained_columns']

            # Add all foreign key constraints at table level
            fks = inspector.get_foreign_keys(table_name)
            if fks:
                table_info["foreign_keys"] = []
                for fk in fks:
                    table_info["foreign_keys"].append({
                        "constrained_columns": fk['constrained_columns'],
                        "referred_table": fk['referred_table'],
                        "referred_columns": fk['referred_columns']
                    })

            db_schema["tables"].append(table_info)

        return db_schema

    except OperationalError as e:
        # Catch DB connection errors
        return {"status": "error", "message": f"DB connection failed during mapping: {e}"}
    except Exception as e:
        # Catch other unexpected errors
        return {"status": "error", "message": f"An unexpected error occurred during database mapping: {e}"}

@app.get("/check-storage")
def check_storage():
    status = check_bucket_access()
    return {
        "bucket": bucket_name,
        "status": "accessible" if status else "unreachable"
    }