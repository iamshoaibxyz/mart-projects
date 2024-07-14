from passlib import context

pwd_contex = context.CryptContext(schemes=["bcrypt"], deprecated="auto")\


def hashedPassword(plain_password: str):
    return pwd_contex.hash(plain_password)

def verify_hashed_password(plain_password: str, hashed_password: str):
    return pwd_contex.verify(plain_password, hashed_password)

# def decode_access_token(token: str):
#     """
#     Decodes a JWT access token.

#     Args:
#         token (str): The JWT token to decode.

#     Returns:
#         dict: The decoded token payload.

#     Raises:
#         HTTPException: If the token is expired, invalid, or any other JWT-related error occurs.
#     """
#     try:
#         # Decode the token using the secret key and the specified algorithm
#         return jwt.decode(token, SECRET_TOKEN, algorithms=[TOKEN_ALGROITHM])
#     except jwt.ExpiredSignatureError as e:
#         # Token has expired
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
#     except jwt.InvalidTokenError as e:
#         # Token is invalid
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#     except jwt.PyJWTError as e:
#         # General JWT error
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token error")
#     except Exception as e:
#         # Any other exception
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

