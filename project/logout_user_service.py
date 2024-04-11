import prisma
import prisma.models
from pydantic import BaseModel


class LogoutUserResponse(BaseModel):
    """
    Response model for a successful logout operation, indicating termination of the user session.
    """

    message: str


async def logout_user(token: str) -> LogoutUserResponse:
    """
    Logs out a user and terminates the session by invalidating the JWT token.

    Args:
        token (str): The JWT token to be invalidated as part of the logout process.

    Returns:
        LogoutUserResponse: Response model for a successful logout operation, indicating termination of the user session.

    This function finds a match for the given token in the AuthToken table, deletes it to invalidate the session,
    and returns a LogoutUserResponse indicating success.
    """
    await prisma.models.AuthToken.prisma().delete_many(where={"token": token})
    return LogoutUserResponse(message="User successfully logged out.")
