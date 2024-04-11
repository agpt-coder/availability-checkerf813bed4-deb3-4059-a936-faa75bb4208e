import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import project.add_integration_service
import project.create_schedule_service
import project.create_user_service
import project.delete_schedule_service
import project.generate_report_service
import project.get_availability_service
import project.get_report_service
import project.get_schedule_service
import project.get_user_profile_service
import project.login_user_service
import project.logout_user_service
import project.refresh_token_service
import project.remove_integration_service
import project.send_notification_service
import project.update_availability_service
import project.update_integration_service
import project.update_notification_preferences_service
import project.update_schedule_service
import project.update_user_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Availability Checker",
    lifespan=lifespan,
    description="To develop a function that returns the real-time availability of professionals, updating based on current activity or schedule, we'll utilize the following tech stack: Python as the programming language, FastAPI for the API framework, PostgreSQL for the database, and Prisma as the ORM. The system will focus on professionals in sectors where immediate response is crucial, such as healthcare, IT support, and customer service. Updates to a professional's availability status will be triggered by various activities including new appointments, meeting completions, and schedule changes.\n\nThe implementation will leverage WebSockets in FastAPI for real-time updates, ensuring a persistent, two-way communication channel. For storing and tracking dynamic schedules and availability, PostgreSQL's robust features like triggers and stored procedures will be utilized. Prisma ORM will facilitate efficient database interactions. The solution will enable manual updates by professionals for flexibility, complemented by automation for predictable or recurring changes. Best practices such as using a publish-subscribe pattern, ensuring secure data transmission, and implementing throttling will be followed to optimize performance and user experience. This will enable a seamless integration of real-time functionality, enhancing workflow coordination and reducing downtime in critical operations.",
)


@app.post("/user", response_model=project.create_user_service.CreateUserProfileResponse)
async def api_post_create_user(
    email: str, password: str, firstName: str, lastName: str, role: prisma.enums.Role
) -> project.create_user_service.CreateUserProfileResponse | Response:
    """
    Creates a new user profile.
    """
    try:
        res = project.create_user_service.create_user(
            email, password, firstName, lastName, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/notification/send",
    response_model=project.send_notification_service.SendNotificationOutput,
)
async def api_post_send_notification(
    recipient_id: str, message: str, channels: List[str]
) -> project.send_notification_service.SendNotificationOutput | Response:
    """
    Sends a notification to a specific user or group of users.
    """
    try:
        res = await project.send_notification_service.send_notification(
            recipient_id, message, channels
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/logout", response_model=project.logout_user_service.LogoutUserResponse)
async def api_post_logout_user(
    token: str,
) -> project.logout_user_service.LogoutUserResponse | Response:
    """
    Logs out a user and terminates the session.
    """
    try:
        res = await project.logout_user_service.logout_user(token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/integration/add",
    response_model=project.add_integration_service.AddIntegrationResponse,
)
async def api_post_add_integration(
    userId: str,
    service: str,
    accessToken: str,
    refreshToken: Optional[str],
    expiryDate: Optional[str],
) -> project.add_integration_service.AddIntegrationResponse | Response:
    """
    Adds a new external service integration.
    """
    try:
        res = await project.add_integration_service.add_integration(
            userId, service, accessToken, refreshToken, expiryDate
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/{id}", response_model=project.update_user_service.UpdateUserProfileResponse
)
async def api_put_update_user(
    id: str,
    email: Optional[str],
    firstName: Optional[str],
    lastName: Optional[str],
    role: Optional[str],
) -> project.update_user_service.UpdateUserProfileResponse | Response:
    """
    Updates an existing user profile.
    """
    try:
        res = await project.update_user_service.update_user(
            id, email, firstName, lastName, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/notification/preferences/update",
    response_model=project.update_notification_preferences_service.UpdateNotificationPreferencesResponse,
)
async def api_put_update_notification_preferences(
    user_id: str,
    email_notifications: bool,
    sms_notifications: bool,
    in_app_notifications: bool,
) -> project.update_notification_preferences_service.UpdateNotificationPreferencesResponse | Response:
    """
    Updates user notification preferences.
    """
    try:
        res = await project.update_notification_preferences_service.update_notification_preferences(
            user_id, email_notifications, sms_notifications, in_app_notifications
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/{id}", response_model=project.get_user_profile_service.UserProfileResponse
)
async def api_get_get_user_profile(
    id: str,
) -> project.get_user_profile_service.UserProfileResponse | Response:
    """
    Retrieves a user's profile information.
    """
    try:
        res = await project.get_user_profile_service.get_user_profile(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/schedule/{id}",
    response_model=project.delete_schedule_service.DeleteScheduleResponse,
)
async def api_delete_delete_schedule(
    id: str,
) -> project.delete_schedule_service.DeleteScheduleResponse | Response:
    """
    Deletes a specified schedule or appointment.
    """
    try:
        res = await project.delete_schedule_service.delete_schedule(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/integration/{id}/update",
    response_model=project.update_integration_service.IntegrationUpdateResponse,
)
async def api_put_update_integration(
    id: str,
    service: str,
    accessToken: str,
    refreshToken: Optional[str],
    expiryDate: datetime,
) -> project.update_integration_service.IntegrationUpdateResponse | Response:
    """
    Updates an existing external service integration.
    """
    try:
        res = await project.update_integration_service.update_integration(
            id, service, accessToken, refreshToken, expiryDate
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/integration/{id}/remove",
    response_model=project.remove_integration_service.RemoveIntegrationResponse,
)
async def api_delete_remove_integration(
    id: str,
) -> project.remove_integration_service.RemoveIntegrationResponse | Response:
    """
    Removes an external service integration.
    """
    try:
        res = await project.remove_integration_service.remove_integration(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/refresh", response_model=project.refresh_token_service.RefreshTokenResponse
)
async def api_post_refresh_token(
    refresh_token: str,
) -> project.refresh_token_service.RefreshTokenResponse | Response:
    """
    Refreshes an expired JWT token using a refresh token.
    """
    try:
        res = await project.refresh_token_service.refresh_token(refresh_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/availability/{userId}",
    response_model=project.get_availability_service.GetAvailabilityResponse,
)
async def api_get_get_availability(
    userId: str,
) -> project.get_availability_service.GetAvailabilityResponse | Response:
    """
    Retrieves the current availability status of a professional.
    """
    try:
        res = await project.get_availability_service.get_availability(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/report/generate",
    response_model=project.generate_report_service.GenerateReportResponse,
)
async def api_post_generate_report(
    userId: str, startDate: str, endDate: str, dataPoints: List[str], reportType: str
) -> project.generate_report_service.GenerateReportResponse | Response:
    """
    Generates a customized report based on user-selected criteria.
    """
    try:
        res = await project.generate_report_service.generate_report(
            userId, startDate, endDate, dataPoints, reportType
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/schedule", response_model=project.create_schedule_service.CreateScheduleOutput
)
async def api_post_create_schedule(
    userId: str,
    startTime: datetime,
    endTime: datetime,
    title: str,
    description: Optional[str],
    available: bool,
) -> project.create_schedule_service.CreateScheduleOutput | Response:
    """
    Creates a new schedule or appointment.
    """
    try:
        res = await project.create_schedule_service.create_schedule(
            userId, startTime, endTime, title, description, available
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/report/{id}", response_model=project.get_report_service.ReportDetails)
async def api_get_get_report(
    id: str,
) -> project.get_report_service.ReportDetails | Response:
    """
    Retrieves a previously generated report.
    """
    try:
        res = await project.get_report_service.get_report(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/availability/update",
    response_model=project.update_availability_service.UpdateAvailabilityResponse,
)
async def api_post_update_availability(
    professional_id: str, new_availability: bool
) -> project.update_availability_service.UpdateAvailabilityResponse | Response:
    """
    Manually updates a professional's availability status.
    """
    try:
        res = await project.update_availability_service.update_availability(
            professional_id, new_availability
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/schedule/{id}",
    response_model=project.update_schedule_service.UpdateScheduleResponse,
)
async def api_put_update_schedule(
    id: str,
    startTime: datetime,
    endTime: datetime,
    title: str,
    description: str,
    available: bool,
) -> project.update_schedule_service.UpdateScheduleResponse | Response:
    """
    Updates an existing schedule or appointment.
    """
    try:
        res = await project.update_schedule_service.update_schedule(
            id, startTime, endTime, title, description, available
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.login_user_service.UserLoginResponse)
async def api_post_login_user(
    email: str, password: str
) -> project.login_user_service.UserLoginResponse | Response:
    """
    Authenticates a user and returns a JWT token.
    """
    try:
        res = await project.login_user_service.login_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/schedule/{id}", response_model=project.get_schedule_service.GetScheduleResponse
)
async def api_get_get_schedule(
    id: str,
) -> project.get_schedule_service.GetScheduleResponse | Response:
    """
    Retrieves the details of a specific schedule or appointment.
    """
    try:
        res = await project.get_schedule_service.get_schedule(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
