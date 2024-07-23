from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ScheduledContent(BaseModel):
    """
    Details of a single scheduled content item.
    """

    content_id: str
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None


class ListScheduledContentResponse(BaseModel):
    """
    The response model outputs a list of all content currently scheduled for display, including details such as content ID, title, description, and the scheduled start and end dates.
    """

    scheduled_contents: List[ScheduledContent]


async def list_scheduled_content() -> ListScheduledContentResponse:
    """
    List all content currently scheduled for display.

    Args:

    Returns:
    ListScheduledNodeContentResponse: The response model outputs a list of all content currently scheduled for display, including details such as content ID, title, description, and the scheduled start and end dates.
    """
    schedules = await prisma.models.ContentSchedule.prisma().find_many(
        where={"active": True}, include={"Content": True}
    )
    scheduled_contents = []
    for schedule in schedules:
        content = schedule.Content
        if content:
            scheduled_content = ScheduledContent(
                content_id=content.id,
                title=content.title,
                description=content.description,
                start_date=schedule.start,
                end_date=schedule.end,
            )
            scheduled_contents.append(scheduled_content)
    return ListScheduledContentResponse(scheduled_contents=scheduled_contents)
