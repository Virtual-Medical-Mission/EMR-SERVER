import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# --- Load environment variables from db_keys.env file ---
# Explicitly tell load_dotenv to look for 'db_keys.env'
load_dotenv(dotenv_path='db_keys.env') # <-- THIS IS THE CRITICAL CHANGE

# --- Database Configuration ---
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Ensure all required environment variables are set
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    # The error message also updated to reflect the new filename
    raise ValueError("One or more database environment variables are not set. Check your db_keys.env file.")

# Construct the SQLAlchemy database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
