from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ReportDetails(BaseModel):
    """
    Detailed information of a specific report including content, type and metadata.
    """

    id: str
    userId: str
    content: str
    reportType: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None


async def get_report(id: str) -> ReportDetails:
    """
    Retrieves a previously generated report.

    Args:
        id (str): Unique identifier of the report to retrieve.

    Returns:
        ReportDetails: Detailed information of a specific report including content, type and metadata.
    """
    report = await prisma.models.Report.prisma().find_unique(where={"id": id})
    if report:
        return ReportDetails(
            id=report.id,
            userId=report.userId,
            content=report.content,
            reportType=report.reportType,
            createdAt=report.createdAt,
            updatedAt=report.updatedAt,
        )
    else:
        raise ValueError(f"Report with id {id} not found")
