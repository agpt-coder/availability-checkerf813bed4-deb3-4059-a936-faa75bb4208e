from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateScheduleOutput(BaseModel):
    """
    Output model after successfully creating a new schedule or appointment.
    """

    id: str
    status: str
    message: str


async def create_schedule(
    userId: str,
    startTime: datetime,
    endTime: datetime,
    title: str,
    description: Optional[str],
    available: bool,
) -> CreateScheduleOutput:
    """
    Creates a new schedule or appointment.

    Args:
        userId (str): The unique identifier of the user for whom the schedule is being created.
        startTime (datetime): The start time of the schedule or appointment.
        endTime (datetime): The end time of the schedule or appointment.
        title (str): The title or summary of the schedule or appointment.
        description (Optional[str]): An optional detailed description of the schedule or appointment.
        available (bool): A boolean indicating if the time slot is marking the professional as available or not.

    Returns:
        CreateScheduleOutput: Output model after successfully creating a new schedule or appointment.
    """
    schedule = await prisma.models.Schedule.prisma().create(
        data={
            "userId": userId,
            "startTime": startTime,
            "endTime": endTime,
            "title": title,
            "description": description if description is not None else "",
            "available": available,
        }
    )
    return CreateScheduleOutput(
        id=schedule.id,
        status="Success",
        message=f"Schedule for {title} has been successfully created.",
    )
