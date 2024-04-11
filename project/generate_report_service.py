from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GenerateReportResponse(BaseModel):
    """
    Response model encapsulating the details of the generated report, including a success indicator, report ID, and possibly a URL to download the report.
    """

    success: bool
    reportId: str
    message: str
    reportUrl: Optional[str] = None


async def generate_report(
    userId: str, startDate: str, endDate: str, dataPoints: List[str], reportType: str
) -> GenerateReportResponse:
    """
    Generates a customized report based on user-selected criteria.

    Args:
    userId (str): The unique identifier of the user requesting the report.
    startDate (str): The starting date of the timeframe for the report.
    endDate (str): The ending date of the timeframe for the report.
    dataPoints (List[str]): List of data points that the user wants to include in the report.
    reportType (str): The type of report requested, such as 'Activity', 'SystemUsage', or 'Compliance'.

    Returns:
    GenerateReportResponse: Response model encapsulating the details of the generated report, including a success indicator, report ID, and possibly a URL to download the report.
    """
    try:
        start_date_object = datetime.strptime(startDate, "%Y-%m-%d")
        end_date_object = datetime.strptime(endDate, "%Y-%m-%d")
    except ValueError as e:
        return GenerateReportResponse(
            success=False,
            reportId="",
            message="Invalid date format. Please use YYYY-MM-DD.",
            reportUrl=None,
        )
    if reportType not in prisma.enums.ReportType.__members__:
        return GenerateReportResponse(
            success=False,
            reportId="",
            message="Invalid report type provided.",
            reportUrl=None,
        )
    report_content = f"Report from {startDate} to {endDate} for user {userId} on {', '.join(dataPoints)}."
    try:
        new_report = await prisma.models.Report.prisma().create(
            data={
                "userId": userId,
                "content": report_content,
                "reportType": getattr(prisma.enums.ReportType, reportType),
            }
        )
        report_url = f"http://example.com/reports/{new_report.id}"
        return GenerateReportResponse(
            success=True,
            reportId=new_report.id,
            message="Report generated successfully.",
            reportUrl=report_url,
        )
    except Exception as err:
        return GenerateReportResponse(
            success=False,
            reportId="",
            message=f"Error creating report: {str(err)}",
            reportUrl=None,
        )
