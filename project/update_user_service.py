from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    Confirms the updated fields of the user's profile, along with any other pertinent information reflecting the changes.
    """

    id: str
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    role: Optional[str] = None
    updateStatus: str


async def update_user(
    id: str,
    email: Optional[str],
    firstName: Optional[str],
    lastName: Optional[str],
    role: Optional[str],
) -> UpdateUserProfileResponse:
    """
    Updates an existing user profile.

    Args:
        id (str): The unique identifier for the user whose profile is being updated.
        email (Optional[str]): The updated email address for the user.
        firstName (Optional[str]): The user's updated first name.
        lastName (Optional[str]): The user's updated last name.
        role (Optional[str]): The updated role of the user, reflecting their position (Professional, Administrator, ITSupport).

    Returns:
        UpdateUserProfileResponse: Confirms the updated fields of the user's profile, along with any other pertinent information reflecting the changes.
    """
    update_payload = {}
    profile_payload = {}
    if email is not None:
        update_payload["email"] = email
    if role is not None:
        update_payload["role"] = role
    if firstName or lastName:
        profile = await prisma.models.Profile.prisma().find_unique(where={"userId": id})
        if profile:
            if firstName is not None:
                profile_payload["firstName"] = firstName
            if lastName is not None:
                profile_payload["lastName"] = lastName
            await prisma.models.Profile.prisma().update(
                where={"userId": id}, data=profile_payload
            )
    if update_payload:
        user = await prisma.models.User.prisma().update(
            where={"id": id}, data=update_payload
        )
    else:
        user = await prisma.models.User.prisma().find_unique(where={"id": id})
    return UpdateUserProfileResponse(
        id=user.id,
        email=user.email,
        firstName=firstName,
        lastName=lastName,
        role=user.role,
        updateStatus="User profile successfully updated.",
    )
