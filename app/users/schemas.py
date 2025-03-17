from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    hashed_password: str


class UserUpdate(BaseModel):
    email: EmailStr
    username: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
