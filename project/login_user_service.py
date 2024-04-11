from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import prisma
import prisma.models
from jose import jwt
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    This model outlines the response received upon a successful login attempt, primarily containing the JWT token for the user session.
    """

    token: str
    expires_in: int


SECRET_KEY = "your_secret_key_here"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Generates a JWT token for authenticated users.

    Args:
        data (dict): The data to encode in the JWT payload.
        expires_delta (Optional[timedelta]): The expiration time for the token. If not specified, defaults to 15 minutes.

    Returns:
        str: A JWT token string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login_user(email: str, password: str) -> UserLoginResponse:
    """
    Authenticates a user and returns a JWT token.

    Args:
        email (str): The email address of the user attempting to log in.
        password (str): The password of the user, which will be verified against the hashed password stored in the database.

    Returns:
        UserLoginResponse: This model outlines the response received upon a successful login attempt, primarily containing the JWT token for the user session.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user:
        hashed_password = user.password.encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = await create_access_token(
                data={"sub": user.email}, expires_delta=access_token_expires
            )
            return UserLoginResponse(
                token=access_token, expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
    raise Exception("Invalid login credentials.")
