from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class PeripheralDeviceTypeDetail(BaseModel):
    """
    Details of a peripheral device type supported by the system.
    """

    name: str
    type: prisma.enums.PeripheralDeviceType


class ListSupportedPeripheralsResponse(BaseModel):
    """
    Provides a list of all supported peripheral devices. Each device type is represented with its name and type as defined in the `prisma.enums.PeripheralDeviceType` enum.
    """

    supported_peripherals: List[PeripheralDeviceTypeDetail]


async def list_supported_peripherals() -> ListSupportedPeripheralsResponse:
    """
    Retrieve a list of supported peripheral devices.

    Args:

    Returns:
    ListSupportedPeripheralsResponse: Provides a list of all supported peripheral devices. Each device type is represented with its name and type as defined in the `prisma.enums.PeripheralDeviceType` enum.
    """
    peripheral_devices = await prisma.models.PeripheralDevice.prisma().find_many()
    peripheral_devices_details = [
        PeripheralDeviceTypeDetail(name=device.name, type=device.type)
        for device in peripheral_devices
    ]
    return ListSupportedPeripheralsResponse(
        supported_peripherals=peripheral_devices_details
    )
