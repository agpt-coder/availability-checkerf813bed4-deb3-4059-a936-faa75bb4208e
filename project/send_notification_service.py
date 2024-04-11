from typing import List, Optional

from pydantic import BaseModel


class SendNotificationOutput(BaseModel):
    """
    Model representing the outcome of sending a notification to the specified recipient(s).
    """

    success: bool
    failed_channels: List[str]
    error_message: Optional[str] = None


async def send_notification(
    recipient_id: str, message: str, channels: List[str]
) -> SendNotificationOutput:
    """
    Sends a notification to a specific user or group of users.

    This function assumes that the different channels ('email', 'sms', 'in_app') have their specific ways of sending notifications in other parts of the system and it emulates the process of sending notifications via these channels.

    Args:
        recipient_id (str): Unique identifier for the recipient or group recipients. This could be a user ID or a group ID depending on the system's design.
        message (str): The message content of the notification to be sent.
        channels (List[str]): A list of channels through which the notification should be sent. Examples: ['email', 'sms', 'in_app']

    Returns:
        SendNotificationOutput: Model representing the outcome of sending a notification to the specified recipient(s).
    """
    failed_channels = []
    for channel in channels:
        try:
            if channel == "email":
                print(f"Sending email to {recipient_id} with message: {message}")
            elif channel == "sms":
                print(f"Sending SMS to {recipient_id} with message: {message}")
            elif channel == "in_app":
                print(
                    f"Sending in-app notification to {recipient_id} with message: {message}"
                )
            else:
                raise ValueError(f"Unsupported channel: {channel}")
        except Exception as e:
            failed_channels.append(channel)
            print(f"Failed to send notification via {channel}, Error: {str(e)}")
    if failed_channels:
        return SendNotificationOutput(
            success=False,
            failed_channels=failed_channels,
            error_message="Some channels failed.",
        )
    else:
        return SendNotificationOutput(success=True, failed_channels=[])
