import prisma
import prisma.models
from pydantic import BaseModel


class DeleteScheduleResponse(BaseModel):
    """
    Provides feedback on the operation's outcome, including confirmation of the deletion or an error message.
    """

    success: bool
    message: str


async def delete_schedule(id: str) -> DeleteScheduleResponse:
    """
    Deletes a specified schedule or appointment.

    Args:
        id (str): The unique identifier of the schedule or appointment to be deleted.

    Returns:
        DeleteScheduleResponse: Provides feedback on the operation's outcome, including confirmation of the deletion or an error message.
    """
    try:
        found_schedule = await prisma.models.Schedule.prisma().find_unique(
            where={"id": id}
        )
        if found_schedule:
            await prisma.models.Schedule.prisma().delete(where={"id": id})
            return DeleteScheduleResponse(
                success=True, message="Schedule deleted successfully"
            )
        else:
            return DeleteScheduleResponse(success=False, message="Schedule not found")
    except Exception as e:
        return DeleteScheduleResponse(success=False, message=str(e))
