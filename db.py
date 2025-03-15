import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

# Read MySQL ConfigMap key pair values from environment variables
db_user = os.getenv("USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("HOST")
db_name = os.getenv("DATABASE")
db_port = os.getenv("PORT", "3306")

# Construct the MySQL database URL
database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

class Model(DeclarativeBase):
    __abstract__ = True

# Create the engine using the constructed database URL
engine = create_engine(database_url, echo=True)
