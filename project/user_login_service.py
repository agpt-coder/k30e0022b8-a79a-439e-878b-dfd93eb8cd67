from datetime import datetime, timedelta

import prisma
import prisma.enums
import prisma.models
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class User(BaseModel):
    """
    The User object model captures basic information about the authenticated user, such as their username and roles.
    """

    id: str
    username: str
    role: prisma.enums.UserRole


class LoginResponse(BaseModel):
    """
    This model represents the response returned upon a successful authentication attempt. It includes a session token which is used for maintaining the user's session across the system.
    """

    token: str
    user: User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def user_login(username: str, password: str) -> LoginResponse:
    """
    Authenticate a user and return a session token.

    Args:
    username (str): The username of the user attempting to log in. In most cases, this could also be the user's email address.
    password (str): The password for the user attempting to log in. It is expected that the password is transmitted securely and encrypted at rest.

    Returns:
    LoginResponse: This model represents the response returned upon a successful authentication attempt. It includes a session token which is used for maintaining the user's session across the system.

    Raises:
    ValueError: If authentication fails due to incorrect username or password.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if not user or not pwd_context.verify(password, user.password):
        raise ValueError("Incorrect username or password")
    user_data = User(id=user.id, username=user.email, role=user.role)
    token_expiration = timedelta(hours=1)
    payload = {
        "sub": user.id,
        "exp": datetime.utcnow() + token_expiration,
        "username": user.email,
        "role": user.role.name
        if isinstance(user.role, prisma.enums.UserRole)
        else user.role,
    }
    token = jwt.encode(payload, "SECRET_KEY", algorithm="HS256")
    return LoginResponse(token=token, user=user_data)
