from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    model_config = {"from_attributes": True}

    name: str | None = None
    email: EmailStr


class CreateUser(UserBase):
    password: str = Field(min_length=8)


class UserPublic(BaseModel):
    model_config = {"from_attributes": True}

    name: str


class UserPrivate(UserPublic):

    id: UUID4
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserUpdate(UserBase):
    pass
