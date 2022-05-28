import typing


class HelixAPIError(BaseException):
    """Base class for Helix API errors"""

    def __init__(self, response, message=''):
        message += f"API Status code = {response['status']}; " if 'status' in response else ''
        message += f"API Error = {response['error']}; " if 'error' in response else ''
        message += f"API Error message = {response['message']}; " if 'message' in response else ''
        self.message = message
        super().__init__(self.message)


class AuthentificationError(HelixAPIError):
    def __init__(self, response):
        self.status_code = 401
        self.message = f"Access token invalid. You’ll need to get a new access token using the appropriate flow for your app. "\
                     + f"Access and refresh token can become invalid for the following reasons: "\
                     + f"1.The token expired; 2.User changes their password; 3.Twitch revokes the token; "\
                     + f"4.User disconnects your app; \n"
        super().__init__(response=response, message=self.message)


class UserNotFoundError(HelixAPIError):
    def __init__(self, response):
        self.message = f"User not found "
        super().__init__(response=response, message=self.message)
