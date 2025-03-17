from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str


class UserUpdate(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
