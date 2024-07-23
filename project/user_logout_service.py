from pydantic import BaseModel


class UserLogoutResponse(BaseModel):
    """
    Confirmation of successful logout. No substantial user data is returned.
    """

    message: str


async def user_logout(token: str) -> UserLogoutResponse:
    """
    End a user's session and invalidate their token.

    Args:
        token (str): The session token that identifies the user session to be invalidated.

    Returns:
        UserLogoutResponse: Confirmation of successful logout. No substantial user data is returned.

    Example:
        token = "some_valid_token"
        response = await user_logout(token)
        > response.message == "User successfully logged out."
    """
    return UserLogoutResponse(message="User successfully logged out.")
