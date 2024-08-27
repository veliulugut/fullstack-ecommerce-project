import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2 as db

load_dotenv()

# Çevre değişkenlerini alın
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# PostgreSQL bağlantı dizesini oluşturun
database_connection = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

print(f"Database connection URL: {database_connection}")

try:
    # Bağlantıyı kontrol et
    conn = db.connect(
        host=DB_HOST,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=DB_PORT
    )
    print("Database connection was successful")
    conn.close()
except db.OperationalError as e:
    print(f"Error connecting to database: {e}")

# SQLAlchemy yapılandırmasını oluşturun
engine = create_engine(database_connection)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()