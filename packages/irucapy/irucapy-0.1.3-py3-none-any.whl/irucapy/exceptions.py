class NetworkError(Exception):
    """
    A network error while accessing the API.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class RoomNotFoundError(Exception):
    """
    A room is not found.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class MemberNotFoundError(Exception):
    """
    A member is not found.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
