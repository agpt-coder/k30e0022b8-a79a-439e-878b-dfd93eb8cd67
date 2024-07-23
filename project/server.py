import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import prisma
import prisma.enums
import project.add_new_device_service
import project.list_scheduled_content_service
import project.list_supported_peripherals_service
import project.update_content_schedule_service
import project.user_login_service
import project.user_logout_service
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
    title="k3",
    lifespan=lifespan,
    description="Based on the information gathered, the kiosk management application requirements include a number of diverse and complex features tailored to a municipal environment. The application requires compatibility with various operating systems such as Windows, macOS, and Linux to ensure broad accessibility. It must support a wide range of peripheral hardware including keyboards, mice, monitors, printers, USB storage devices, barcode scanners, and RFID readers, catering to different user and operational needs.\n\nFor security, the application will incorporate strong user authentication mechanisms favoring OAuth 2.0 and JWT for API security, coupled with AES for data encryption, to protect sensitive information both at rest and in transit. Additional security measures include robust access control, regular updates and patch management, comprehensive encryption, firewalls, and intrusion detection systems.\n\nThe UI must adhere to existing branding guidelines, offering customization options for colors, fonts, and logos. It will also feature multilingual support, potentially leveraging APIs like Google Translate or Microsoft Translator for dynamic translations, ensuring accessibility and usability across different cultures and languages.\n\nThe core functionality revolves around a customizable UI for displaying media and information with options for interactivity and accessibility. A local CMS will manage content scheduling and updates, capable of operating in offline modes with efficient data synchronization once connectivity is restored. Real-time device monitoring and remote management within the local network are crucial for operational integrity and responsiveness.\n\nAnalyses and reporting capabilities will focus on generating insights into user engagement and app performance. These features, alongside offline support functionalities, will be critical in enabling the application to deliver content and services uninterrupted, even in fluctuated network conditions.\n\nDevelopment will adopt a human-in-the-loop approach to ensure the final product align to real-world usability and requirements, utilizing agile methodologies for continuous iteration. Recursive programming techniques will be employed to handle the inherent complexity of the application's functionality, especially in managing the customizable UI components and the local CMS.\n\nThe technology stack will include Python, FastAPI, PostgreSQL, and Prisma to ensure the application is built with modern, efficient technologies that support the ambitious feature set required. The proposed design and development strategies aim to result in an intuitive, secure, and versatile kiosk management system that meets the specific needs of the municipal server environment.",
)


@app.post("/auth/logout", response_model=project.user_logout_service.UserLogoutResponse)
async def api_post_user_logout(
    token: str,
) -> project.user_logout_service.UserLogoutResponse | Response:
    """
    End a user's session and invalidate their token.
    """
    try:
        res = await project.user_logout_service.user_logout(token)
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
    "/content/schedule",
    response_model=project.update_content_schedule_service.UpdateContentScheduleResponse,
)
async def api_post_update_content_schedule(
    contentId: str, start: datetime, end: Optional[datetime]
) -> project.update_content_schedule_service.UpdateContentScheduleResponse | Response:
    """
    Update the scheduling information for a piece of content.
    """
    try:
        res = await project.update_content_schedule_service.update_content_schedule(
            contentId, start, end
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
    "/api/peripherals",
    response_model=project.add_new_device_service.AddNewDeviceResponse,
)
async def api_post_add_new_device(
    name: str, type: prisma.enums.PeripheralDeviceType
) -> project.add_new_device_service.AddNewDeviceResponse | Response:
    """
    Register a new peripheral device with the kiosk.
    """
    try:
        res = await project.add_new_device_service.add_new_device(name, type)
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
    "/api/peripherals",
    response_model=project.list_supported_peripherals_service.ListSupportedPeripheralsResponse,
)
async def api_get_list_supported_peripherals() -> project.list_supported_peripherals_service.ListSupportedPeripheralsResponse | Response:
    """
    Retrieve a list of supported peripheral devices.
    """
    try:
        res = (
            await project.list_supported_peripherals_service.list_supported_peripherals()
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
    "/content/scheduled",
    response_model=project.list_scheduled_content_service.ListScheduledContentResponse,
)
async def api_get_list_scheduled_content() -> project.list_scheduled_content_service.ListScheduledContentResponse | Response:
    """
    List all content currently scheduled for display.
    """
    try:
        res = await project.list_scheduled_content_service.list_scheduled_content()
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


@app.post("/auth/login", response_model=project.user_login_service.LoginResponse)
async def api_post_user_login(
    username: str, password: str
) -> project.user_login_service.LoginResponse | Response:
    """
    Authenticate a user and return a session token.
    """
    try:
        res = await project.user_login_service.user_login(username, password)
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
