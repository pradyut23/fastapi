from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

Engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)  #Database session

Base = declarative_base()  #Class which will be inherited to create each database model or classes


#Dependency
def get_db():  # Get a session to the database and close it once request completed
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''
#To connect to the database directly without sqlalchemy

import time
import psycopg2
from psycopg2.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
        password='root', cursor_factory=RealDictCursor) #cursor_facory just gives the column names with the values, without this the cursor will only return the values without the column name it is mapped to
        cursor = conn.cursor() #will be used to execute sql statements
        print("Database connection succesful!")
        break
    except Exception as error:
        print("Connection to database failed!")
        print('Error:', error)
        time.sleep(2)
'''
