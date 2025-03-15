import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from models import Base, Todo, User


db_user = os.getenv("USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("HOST")
db_name = os.getenv("DATABASE")
db_port = os.getenv("PORT", "3306")

database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"



db = SQLAlchemy(Base)

class DBContext():
    def __init__(self, app):
        self.db = SQLAlchemy(Base)
        self.engine = create_engine(database_url, echo=True)
        self.connection = self.engine.connect()
        self.create_database()
        self.db.init_app(app)

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
    


