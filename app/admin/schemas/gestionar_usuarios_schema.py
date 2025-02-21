from pydantic import BaseModel, EmailStr


class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class UserResponseSinRole(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class UserCreateAdmin(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # "Admin" o "User"
