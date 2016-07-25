from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
# from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///usersdb.db', echo=True)
Base = declarative_base()

class User(Base):
  
    __tablename__ = "users"
  
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(String)
#     pw_hash = Column(String)
     
    def __init__(self, username, password,email,role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        
#     def set_password(self, password):
#         self.password = generate_password_hash(password)
#             
#     def check_password(self, password):
#         return check_password_hash(self.password, password)
  
# create tables
Base.metadata.create_all(engine)
