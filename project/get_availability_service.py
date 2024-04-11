from datetime import datetime, timezone
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GetAvailabilityResponse(BaseModel):
    """
    The output model that provides the current availability status of the requested professional. It encapsulates whether the professional is currently available and any relevant message or detail that might explain their availability state.
    """

    userId: str
    isAvailable: bool
    message: Optional[str] = None
    timeUntilNextAvailability: Optional[int] = None


async def get_availability(userId: str) -> GetAvailabilityResponse:
    """
    Retrieves the current availability status of a professional.

    Args:
        userId (str): The unique identifier of the professional whose availability status is being requested.

    Returns:
        GetAvailabilityResponse: The output model that provides the current availability status of the requested professional. It encapsulates whether the professional is currently available and any relevant message or detail that might explain their availability state.
    """
    now = datetime.now(timezone.utc)
    current_schedule = await prisma.models.Schedule.prisma().find_first(
        where={"userId": userId, "startTime": {"lte": now}, "endTime": {"gte": now}},
        include={"Appointment": True},
    )
    if current_schedule:
        if current_schedule.available and (not current_schedule.Appointment):
            return GetAvailabilityResponse(
                userId=userId, isAvailable=True, message="Available"
            )
        else:
            next_available_schedule = await prisma.models.Schedule.prisma().find_first(
                where={"userId": userId, "startTime": {"gt": now}, "available": True},
                order={"startTime": "asc"},
            )
            if next_available_schedule:
                time_until_next = (
                    next_available_schedule.startTime - now
                ).total_seconds()
                return GetAvailabilityResponse(
                    userId=userId,
                    isAvailable=False,
                    message=f"Unavailable until {next_available_schedule.startTime.strftime('%Y-%m-%d %H:%M')}",
                    timeUntilNextAvailability=int(time_until_next / 60),
                )
            else:
                return GetAvailabilityResponse(
                    userId=userId,
                    isAvailable=False,
                    message="No more available schedules today",
                )
    else:
        return GetAvailabilityResponse(
            userId=userId, isAvailable=False, message="No current schedules found"
        )
