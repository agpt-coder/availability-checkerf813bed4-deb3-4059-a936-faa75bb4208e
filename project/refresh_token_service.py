from datetime import datetime, timedelta

import prisma
import prisma.models
from jose import jwt
from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    """
    Response model for the refresh token operation, providing a new JWT token for continued authentication.
    """

    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


async def refresh_token(refresh_token: str) -> RefreshTokenResponse:
    """
    Refreshes an expired JWT token using a refresh token.

    The function searches for the refresh token provided in the database, validates it,
    generates a new access token and optionally a new refresh token for the user.

    Args:
        refresh_token (str): The refresh token issued to the user during the login or previous token refresh operation.

    Returns:
        RefreshTokenResponse: Response model for the refresh token operation, providing a new JWT token for continued authentication.

    Raises:
        ValueError: If the refresh token is not found or is invalid.
    """
    SECRET_KEY = "your_super_secret_key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    auth_token = await prisma.models.AuthToken.prisma().find_unique(
        where={"token": refresh_token}, include={"User": True}
    )
    if auth_token is None or datetime.utcnow() > auth_token.expiryDate:
        raise ValueError("Refresh token is invalid or has expired.")
    access_token_expires = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = jwt.encode(
        {"sub": auth_token.User.id, "exp": access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    refresh_token_expires = datetime.utcnow() + timedelta(days=30)
    new_refresh_token = jwt.encode(
        {"sub": auth_token.User.id, "exp": refresh_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    await prisma.models.AuthToken.prisma().update(
        where={"id": auth_token.id},
        data={"token": new_refresh_token, "expiryDate": refresh_token_expires},
    )
    return RefreshTokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
