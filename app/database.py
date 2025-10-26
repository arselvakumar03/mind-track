
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


DB_HOST = "192.168.0.6"
DB_NAME = "mindTrack"
DB_USER = "postgres"
DB_PASSWORD = "passw0rd123"
DB_PORT = 5432

URL_DATABASE = f"postgresql://postgres:passw0rd123@192.168.0.6:5432/mindTrack"
#URL_DATABASE = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()