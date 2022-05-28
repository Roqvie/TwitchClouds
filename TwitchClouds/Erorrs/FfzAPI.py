import typing


class BaseFfzAPIError(BaseException):
    def __init__(self, response, message=''):
        message += f"API Status code = {response['status']}; " if 'status' in response else ''
        message += f"API Error = {response['error']}; " if 'error' in response else ''
        message += f"API Error message = {response['message']}; " if 'message' in response else ''
        self.message = message
        super().__init__(self.message)