import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class AddNewDeviceResponse(BaseModel):
    """
    Confirms the successful registration of the peripheral device, including its ID and a status message.
    """

    device_id: str
    status: str


async def add_new_device(
    name: str, type: prisma.enums.PeripheralDeviceType
) -> AddNewDeviceResponse:
    """
    Register a new peripheral device with the kiosk.

    Args:
        name (str): The name of the peripheral device, descriptive enough for identification purposes.
        type (PeripheralDeviceType): The type of the peripheral device, aligned with the predefined device types.

    Returns:
        AddNewDeviceResponse: Confirms the successful registration of the peripheral device, including its ID and a status message.
    """
    try:
        new_device = await prisma.models.PeripheralDevice.prisma().create(
            data={"name": name, "type": type}
        )
        response = AddNewDeviceResponse(device_id=new_device.id, status="success")
    except Exception as error:
        print(f"Error registering device: {error}")
        response = AddNewDeviceResponse(device_id="", status="error")
    return response
