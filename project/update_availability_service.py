from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateAvailabilityResponse(BaseModel):
    """
    The response to a request to update a professional's availability status. It confirms the update and reflects the new status.
    """

    success: bool
    updated_availability: bool
    message: Optional[str] = None


async def update_availability(
    professional_id: str, new_availability: bool
) -> UpdateAvailabilityResponse:
    """
    Manually updates a professional's availability status.

    Args:
        professional_id (str): The unique identifier for the professional whose availability is being updated.
        new_availability (bool): The new availability status for the professional. It should indicate if the professional is now available or not.

    Returns:
        UpdateAvailabilityResponse: The response to a request to update a professional's availability status. It confirms the update and reflects the new status.

    Example:
        professional_id = "some-unique-professional-id"
        new_availability = True
        response = await update_availability(professional_id, new_availability)
        print(response)
        > {'success': True, 'updated_availability': True, 'message': "Professional's availability status updated successfully."}
    """
    try:
        await prisma.models.Schedule.prisma().update_many(
            where={"userId": professional_id, "endTime": {"gt": datetime.now()}},
            data={"available": new_availability},
        )
        return UpdateAvailabilityResponse(
            success=True,
            updated_availability=new_availability,
            message="Professional's availability status updated successfully.",
        )
    except Exception as e:
        return UpdateAvailabilityResponse(
            success=False,
            updated_availability=new_availability,
            message=f"Failed to update availability status due to an error: {str(e)}",
        )
