from .utils import color


class ServiceError(Exception):
    """ Common exception """
    code = 420

    def __init__(self, msg=None, error=None):
        self.msg = str(error) if msg is None and error else msg
        self.error = self.__class__.__name__ if error is None else error.__class__.__name__
        super().__init__(self.msg)

    def __str__(self):
        msg = color.r(self.error)

        if self.msg:
            msg += color.r(f": {self.msg}")

        return msg

    def __repr__(self):
        return self.__str__()


class ApiError(ServiceError):
    code = 422


class SteamApiError(ApiError):
    code = 501


class SteamApiNotFoundError(SteamApiError):
    code = 404


class NotionApiError(ApiError):
    code = 502
