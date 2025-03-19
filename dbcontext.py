import os
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from models import Base, Todo, User

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Fetch environment variables with default values
db_user = os.getenv("USER", "root")
db_password = os.getenv("MYSQL_PASSWORD", "password")
db_host = os.getenv("HOST", "127.0.0.1")
db_name = os.getenv("DATABASE", "lab8_db")
db_port = os.getenv("PORT", "43115")

# Debug: Print environment variables
print(f"db_user: {db_user}")
print(f"db_password: {db_password}")
print(f"db_host: {db_host}")
print(f"db_name: {db_name}")
print(f"db_port: {db_port}")

# Fetch SSL environment variables with default values from configmap
ssl_ca = os.getenv("SSL_CA", "/etc/mysql-ssl/ca-cert.pem")
ssl_cert = os.getenv("SSL_CERT", "/etc/mysql-ssl/client-cert.pem")
ssl_key = os.getenv("SSL_KEY", "/etc/mysql-ssl/client-key.pem")

# Debug: Print SSL environment variables
print(f"ssl_ca: {ssl_ca}")
print(f"ssl_cert: {ssl_cert}")
print(f"ssl_key: {ssl_key}")

# Check if any of the required environment variables are missing
if not all([db_user, db_password, db_host, db_name, db_port]):
    raise EnvironmentError("One or more required environment variables are missing")

# Create a database URL without specifying the database name
database_url_without_db = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/"

# Create a database URL with SSL parameters
database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?ssl_ca={ssl_ca}&ssl_cert={ssl_cert}&ssl_key={ssl_key}"

# Debug: Print database URLs
print(f"database_url_without_db: {database_url_without_db}")
print(f"database_url: {database_url}")

# Retry mechanism
max_retries = 5
retry_delay = 5  # seconds

for attempt in range(max_retries):
    try:
        # Create the database if it does not exist
        engine = create_engine(database_url_without_db, echo=True, pool_pre_ping=True, pool_recycle=280)
        print(engine.__str__())
        with engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Could not create the database.")
            raise

# Initialize SQLAlchemy with the Flask app instance
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)

class DBContext():
    def __init__(self, app):
        self.db = db  # Use the already initialized db object
        try:
            self.engine = create_engine(database_url)
            # Retry mechanism for engine.connect()
            for attempt in range(max_retries):
                try:
                    self.connection = self.engine.connect()
                    break
                except Exception as e:
                    print(f"Attempt {attempt + 1} to connect to the database failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                    else:
                        print("Max retries reached. Could not connect to the database.")
                        raise
            self.create_database()
            self.db.init_app(app)
        except Exception as e:
            print(f"Error initializing DBContext: {e}")
            raise

    def create_database(self):
        with self.engine.begin() as connection:
            Base.metadata.create_all(connection, tables=[Todo.__table__, User.__table__])
    
    def getUserList(self):
        return self.db.session.query(User).all()
    
    def addUser(self, user: User):
        self.db.session.add(user)

    def getUser(self, id: int):
        return self.db.session.query(User).filter(User.ID == id).first()
    
    def deleteUser(self, id: int):
        user = self.getUser(id)
        self.db.session.delete(user)

    def updateUser(self, id: int, user: User):
        self.db.session.query(User).filter(User.ID == id).update(user)

    def close(self):
        self.db.session.commit()  # Commit any pending transactions
        self.db.session.close()   # Close the session
        self.connection.close()   # Close the connection



