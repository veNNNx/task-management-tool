class UnauthenticatedUserException(Exception):
    def __init__(self) -> None:
        message = "Incorrect email or password"
        super().__init__(message)
