from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserIn(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: UUID
    email: EmailStr
    name: str
    hashed_password: str
