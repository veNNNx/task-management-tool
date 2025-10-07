from attrs import define


@define
class TokenData:
    email: str | None = None
