import prisma
import prisma.models
from pydantic import BaseModel


class UpdateNotificationPreferencesResponse(BaseModel):
    """
    Confirms that the user's notification preferences have been updated.
    """

    user_id: str
    status: str


async def update_notification_preferences(
    user_id: str,
    email_notifications: bool,
    sms_notifications: bool,
    in_app_notifications: bool,
) -> UpdateNotificationPreferencesResponse:
    """
    Updates user notification preferences.

    This function asynchronously updates the user's preferences for receiving notifications via email, SMS, and in-app.

    Args:
        user_id (str): The unique identifier for the user whose notification preferences are to be updated.
        email_notifications (bool): Whether the user wishes to receive notifications via email.
        sms_notifications (bool): Whether the user wishes to receive notifications via SMS.
        in_app_notifications (bool): Whether the user wishes to receive in-app notifications.

    Returns:
        UpdateNotificationPreferencesResponse: Confirms that the user's notification preferences have been updated.

    Example:
        await update_notification_preferences("123e4567-e89b-12d3-a456-426614174000", True, False, True)
        > UpdateNotificationPreferencesResponse(user_id="123e4567-e89b-12d3-a456-426614174000", status="Success")
    """
    try:
        user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
        if not user:
            return UpdateNotificationPreferencesResponse(
                user_id=user_id, status="User not found"
            )
        await prisma.models.Notification.prisma().update_many(
            where={"userId": user_id},
            data={
                "email_notifications": email_notifications,
                "sms_notifications": sms_notifications,
                "in_app_notifications": in_app_notifications,
            },
        )
        return UpdateNotificationPreferencesResponse(user_id=user_id, status="Success")
    except Exception as e:
        return UpdateNotificationPreferencesResponse(
            user_id=user_id, status=f"Failure: {str(e)}"
        )
