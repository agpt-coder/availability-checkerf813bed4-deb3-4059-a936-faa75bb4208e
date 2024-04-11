from typing import Optional

import prisma
import prisma.models
from dateutil.parser import parse
from pydantic import BaseModel


class AddIntegrationResponse(BaseModel):
    """
    Response model for adding new external service integration. Indicates success and contains the ID of the newly created integration.
    """

    integrationId: str
    success: bool
    message: str


async def add_integration(
    userId: str,
    service: str,
    accessToken: str,
    refreshToken: Optional[str] = None,
    expiryDate: Optional[str] = None,
) -> AddIntegrationResponse:
    """
    Adds a new external service integration.

    Args:
    userId (str): The unique identifier of the user adding the integration.
    service (str): The name of the external service to be integrated, e.g., 'Google Calendar'.
    accessToken (str): The access token provided by the external service for authentication.
    refreshToken (Optional[str]): The refresh token provided by the external service for maintaining prolonged access. Optional.
    expiryDate (Optional[str]): The expiry date of the access token if applicable. Optional.

    Returns:
    AddIntegrationResponse: Response model for adding new external service integration. Indicates success and contains the ID of the newly created integration.
    """
    try:
        expiry_datetime = parse(expiryDate) if expiryDate else None
        new_integration = await prisma.models.Integration.prisma().create(
            data={
                "userId": userId,
                "service": service,
                "accessToken": accessToken,
                "refreshToken": refreshToken,
                "expiryDate": expiry_datetime,
            }
        )
        return AddIntegrationResponse(
            integrationId=new_integration.id,
            success=True,
            message="Integration added successfully.",
        )
    except Exception as e:
        return AddIntegrationResponse(
            integrationId="",
            success=False,
            message=f"Failed to add integration: {str(e)}",
        )
