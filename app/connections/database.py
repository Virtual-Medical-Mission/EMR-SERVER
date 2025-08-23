import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("One or more database environment variables are not set. Check your .env file.")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def test_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT NOW()"))
            current_time = result.scalar()
            return {"status": "success", "db_time": str(current_time)}
    except OperationalError as e:
        return {"status": "error", "message": f"DB connection failed: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {e}"}

def map_database_schema():
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
                    "type": str(column['type']),
                    "nullable": column['nullable'],
                    "primary_key": column['primary_key']
                }
                fk_info = inspector.get_foreign_keys(table_name, column_name=column['name'])
                if fk_info:
                    first_fk = fk_info[0]
                    col_info["foreign_key"] = {
                        "referred_table": first_fk['referred_table'],
                        "referred_column": first_fk['referred_columns'][0]
                    }
                table_info["columns"].append(col_info)

            pks = inspector.get_pk_constraint(table_name)
            if pks and pks['constrained_columns']:
                table_info["primary_key_columns"] = pks['constrained_columns']

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
        return {"status": "error", "message": f"DB connection failed during mapping: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error during mapping: {e}"}
