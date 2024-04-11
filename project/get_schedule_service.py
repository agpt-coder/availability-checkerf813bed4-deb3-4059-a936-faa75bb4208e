from datetime import datetime
from enum import Enum
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserBrief(BaseModel):
    """
    A brief user model providing essential information about the schedule owner.
    """

    userId: str
    email: str
    role: prisma.enums.Role


class AppointmentBrief(BaseModel):
    """
    An appointment model providing essential information about the individual appointments within the schedule.
    """

    appointmentId: str
    title: str
    startTime: datetime
    endTime: datetime
    description: Optional[str] = None


class GetScheduleResponse(BaseModel):
    """
    This model represents the detailed data of a schedule, including associated appointments and minimal user information to avoid redundant data exposure.
    """

    schedule_id: str
    startTime: datetime
    endTime: datetime
    title: str
    description: Optional[str] = None
    available: bool
    user: UserBrief
    appointments: List[AppointmentBrief]


class Role(Enum):
    Professional: str = "Professional"
    Administrator: str = "Administrator"
    ITSupport: str = "ITSupport"


async def get_schedule(id: str) -> GetScheduleResponse:
    """
    Retrieves the details of a specific schedule or appointment.

    Args:
        id (str): This is the unique identifier for each schedule, used to retrieve the specific schedule's details.

    Returns:
        GetScheduleResponse: This model represents the detailed data of a schedule, including associated appointments and minimal user information to avoid redundant data exposure.
    """
    schedule = await prisma.models.Schedule.prisma().find_unique(
        where={"id": id}, include={"User": True, "Appointment": True}
    )
    if schedule is None:
        raise ValueError(f"Schedule with ID {id} not found")
    user_brief = UserBrief(
        userId=schedule.User.id, email=schedule.User.email, role=schedule.User.role.name
    )
    appointments_brief = [
        AppointmentBrief(
            appointmentId=appointment.id,
            title=appointment.title,
            startTime=appointment.startTime,
            endTime=appointment.endTime,
            description=appointment.description,
        )
        for appointment in schedule.Appointment
    ]
    return GetScheduleResponse(
        schedule_id=schedule.id,
        startTime=schedule.startTime,
        endTime=schedule.endTime,
        title=schedule.title,
        description=schedule.description,
        available=schedule.available,
        user=user_brief,
        appointments=appointments_brief,
    )
