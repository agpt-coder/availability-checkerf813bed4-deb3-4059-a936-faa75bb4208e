from enum import Enum
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class NotificationPreferences(BaseModel):
    """
    The user's preferences for receiving notifications.
    """

    email_notifications_enabled: bool
    sms_notifications_enabled: bool
    app_notifications_enabled: bool


class UserProfileResponse(BaseModel):
    """
    Response model containing detailed profile information about a user.
    """

    user_id: str
    email: str
    role: prisma.enums.Role
    first_name: str
    last_name: str
    linked_schedules: List[str]
    notification_preferences: NotificationPreferences


class Role(Enum):
    Professional: str = "Professional"
    Administrator: str = "Administrator"
    ITSupport: str = "ITSupport"


async def get_user_profile(id: str) -> UserProfileResponse:
    """
    Retrieves a user's profile information from the database.

    Args:
        id (str): Unique identifier for the user whose profile is being requested.

    Returns:
        UserProfileResponse: A comprehensive model containing all relevant information about the user.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": id},
        include={"Profile": True, "Schedules": True, "Notification": True},
    )
    if not user:
        raise ValueError("User not found.")
    notification_preferences = NotificationPreferences(
        email_notifications_enabled=any(
            (n.message.startswith("Email:") for n in user.Notification)
        ),
        sms_notifications_enabled=any(
            (n.message.startswith("SMS:") for n in user.Notification)
        ),
        app_notifications_enabled=any(
            (n.message.startswith("App:") for n in user.Notification)
        ),
    )
    return UserProfileResponse(
        user_id=user.id,
        email=user.email,
        role=prisma.enums.Role[user.role],
        first_name=user.Profile.firstName if user.Profile else "",
        last_name=user.Profile.lastName if user.Profile else "",
        linked_schedules=[schedule.id for schedule in user.Schedules],
        notification_preferences=notification_preferences,
    )
