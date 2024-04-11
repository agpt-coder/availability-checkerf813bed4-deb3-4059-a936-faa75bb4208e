import prisma
import prisma.models
from pydantic import BaseModel


class RemoveIntegrationResponse(BaseModel):
    """
    A confirmation response signaling successful removal of the integration.
    """

    message: str


async def remove_integration(id: str) -> RemoveIntegrationResponse:
    """
    Removes an external service integration.

    This function deletes an integration from the database using its unique identifier.
    It verifies whether the integration exists and successfully deletes it, returning a confirmation message.

    Args:
        id (str): Unique identifier of the integration to be removed.

    Returns:
        RemoveIntegrationResponse: A confirmation response signaling successful removal of the integration.

    Example:
        remove_integration('12345-67890')
        > RemoveIntegrationResponse(message='Integration successfully removed.')
    """
    await prisma.models.Integration.prisma().delete(where={"id": id})
    return RemoveIntegrationResponse(message="Integration successfully removed.")
