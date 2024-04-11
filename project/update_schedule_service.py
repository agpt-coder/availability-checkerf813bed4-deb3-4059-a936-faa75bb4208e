from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateScheduleResponse(BaseModel):
    """
    Confirms that the schedule or appointment has been updated successfully.
    """

    success: bool
    message: str


async def update_schedule(
    id: str,
    startTime: datetime,
    endTime: datetime,
    title: str,
    description: str,
    available: bool,
) -> UpdateScheduleResponse:
    """
    Updates an existing schedule or appointment.

    Args:
        id (str): Unique identifier for the specific schedule or appointment.
        startTime (datetime): The start time for the schedule or appointment.
        endTime (datetime): The end time for the schedule or appointment.
        title (str): The title or purpose of the schedule or appointment.
        description (str): Additional details or notes about the schedule or appointment.
        available (bool): Availability status of the professional for this schedule slot. True if available, False otherwise.

    Returns:
        UpdateScheduleResponse: Confirms that the schedule or appointment has been updated successfully.
    """
    try:
        schedule = await prisma.models.Schedule.prisma().find_unique(where={"id": id})
        if not schedule:
            return UpdateScheduleResponse(success=False, message="Schedule not found.")
        await prisma.models.Schedule.prisma().update(
            where={"id": id},
            data={
                "startTime": startTime,
                "endTime": endTime,
                "title": title,
                "description": description,
                "available": available,
            },
        )
        return UpdateScheduleResponse(
            success=True, message="Schedule updated successfully."
        )
    except Exception as e:
        return UpdateScheduleResponse(
            success=False,
            message=f"An error occurred while updating the schedule: {str(e)}",
        )
