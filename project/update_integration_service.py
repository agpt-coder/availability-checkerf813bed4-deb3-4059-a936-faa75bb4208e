from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class IntegrationDetails(BaseModel):
    """
    Detailed representation of an updated external service integration.
    """

    id: str
    service: str
    accessToken: str
    refreshToken: Optional[str] = None
    expiryDate: datetime


class IntegrationUpdateResponse(BaseModel):
    """
    Response model indicating the outcome of the update operation on an external service integration.
    """

    status: str
    updatedIntegration: IntegrationDetails


async def update_integration(
    id: str,
    service: str,
    accessToken: str,
    refreshToken: Optional[str],
    expiryDate: datetime,
) -> IntegrationUpdateResponse:
    """
    Updates an existing external service integration.

    Args:
        id (str): The unique ID of the integration to be updated.
        service (str): The name of the external service.
        accessToken (str): The new access token for the service integration.
        refreshToken (Optional[str]): The new refresh token for the service integration, if available.
        expiryDate (datetime): The new expiry date of the access token.

    Returns:
        IntegrationUpdateResponse: Response model indicating the outcome of the update operation on an external service integration.
    """
    try:
        updated_integration = await prisma.models.Integration.prisma().update(
            where={"id": id},
            data={
                "service": service,
                "accessToken": accessToken,
                "refreshToken": refreshToken,
                "expiryDate": expiryDate,
            },
        )
        return IntegrationUpdateResponse(
            status="success", updatedIntegration=updated_integration
        )
    except Exception as e:
        return IntegrationUpdateResponse(
            status=f"failed: {str(e)}", updatedIntegration=None
        )
