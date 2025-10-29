from uuid import UUID


class UserByEmailNotFoundException(Exception):
    def __init__(self, email: str):
        message = f"No user with {email=} exists in the store!"

        super().__init__(message)


class UserByIdNotFoundException(Exception):
    def __init__(self, id: UUID):
        message = f"No user with {id=} exists in the store!"

        super().__init__(message)


class UserWithEmailAlreadyExistsException(Exception):
    def __init__(self, email: str):
        message = f"The email {email} is already taken!"

        super().__init__(message)
