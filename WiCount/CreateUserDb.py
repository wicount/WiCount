#Uncomment the lines below to allow modules to import successfully on the server
#import sys
#sys.path.insert(0, "/home/student/anaconda3/lib/python3.4/site-packages")

from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from passlib.hash import sha256_crypt

# To connect to users database
engine = create_engine('sqlite:///usersdb.db', echo=True)
Base = declarative_base()

class User(Base):
    # To create users table and define the field names    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)
    email = Column(String)
    role = Column(String)
     
    def __init__(self, username, password,email,role):
        self.username = username
        self.email = email
        self.role = role
        # Encrypt password
        self.password = sha256_crypt.encrypt(password)
        
    def verify(self, password):
        # to verify the password during login
        return sha256_crypt.verify(password, self.password)  
  
# create tables
Base.metadata.create_all(engine)
