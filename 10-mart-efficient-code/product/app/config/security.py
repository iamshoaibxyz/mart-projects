from passlib import context

pwd_contex = context.CryptContext(schemes=["bcrypt"], deprecated="auto")\


def hashedPassword(plain_password: str):
    return pwd_contex.hash(plain_password)

def verify_hashed_password(plain_password: str, hashed_password: str):
    return pwd_contex.verify(plain_password, hashed_password)