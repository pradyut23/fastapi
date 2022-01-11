from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')  #Tells what hashing algo we want to use

def hash(password: str):    #Hashes the pwd
    return pwd_context.hash(password)

def verify(password, hasshed_pwd):      #verifies the plain pwd to it's hash
    return pwd_context.verify(password, hasshed_pwd)