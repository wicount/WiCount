from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from passlib.hash import sha256_crypt

engine = create_engine('sqlite:///usersdb.db', echo=True)
Base = declarative_base()

class User(Base):
  
    __tablename__ = "users"
  
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(String)
     
    def __init__(self, username, password,email,role):
        self.username = username
        self.email = email
        self.role = role
        self.password = sha256_crypt.encrypt(password)
        
    def verify(self, password):
        return sha256_crypt.verify(password, self.password)  

  
# create tables
Base.metadata.create_all(engine)
