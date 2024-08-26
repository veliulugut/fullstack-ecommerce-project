import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

database_connection = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


try:
    conn = psycopg2.connect(database_connection)
    print("Database connected successfully")

    conn.close()

except psycopg2.OperationalError as e:
    print(f"Error connecting to database: {e}")




