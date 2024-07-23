from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateContentScheduleResponse(BaseModel):
    """
    Response model confirming the update of scheduling information, including the content ID and the new scheduling details.
    """

    success: bool
    contentId: str
    start: datetime
    end: Optional[datetime] = None


async def update_content_schedule(
    contentId: str, start: datetime, end: Optional[datetime]
) -> UpdateContentScheduleResponse:
    """
    Update the scheduling information for a piece of content.

    This function looks up the relevant content schedule entry in the database. If an entry is found,
    it updates the start and, if provided, the end date of the schedule. If the schedule does not exist,
    it creates a new schedule entry for the content. The function then returns a response model indicating
    the success of the operation, along with the content ID and the updated scheduling details.

    Args:
    contentId (str): Unique identifier for the content piece being updated.
    start (datetime): Start date and time for when the content should be scheduled to display.
    end (Optional[datetime]): End date and time for when the content should stop being displayed, optional to allow for indefinite display.

    Returns:
    UpdateContentSchedule:: Response model confirming the update of scheduling information, including the content ID and the new scheduling details.

    Example:
        update_content_schedule(
            contentId="123e4567-e89b-12d3-a456-426614174000",
            start=datetime.utcnow(),
            end=None
        )
    """
    schedule = await prisma.models.ContentSchedule.prisma().find_unique(
        where={"contentId": contentId}
    )
    if schedule:
        updated_schedule = await prisma.models.ContentSchedule.prisma().update(
            where={"id": schedule.id}, data={"start": start, "end": end}
        )
    else:
        updated_schedule = await prisma.models.ContentSchedule.prisma().create(
            data={"contentId": contentId, "start": start, "end": end, "active": True}
        )
    return UpdateContentScheduleResponse(
        success=True if updated_schedule else False,
        contentId=contentId,
        start=start,
        end=end,
    )
