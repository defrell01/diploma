from pydantic import BaseModel, EmailStr


class RegUser(BaseModel):
    user_id: int | None = None
    email: EmailStr
    password: str
    phone_number: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    role: str


class User(BaseModel):
    email: EmailStr
    password: str | None = None


class Parent_Request(BaseModel):
    fisrt_name: str | None = None
    second_name: str | None = None
    phone_number: str | None = None
    email: EmailStr
    password: str


class Child_Request(BaseModel):
    fisrt_name: str | None = None
    second_name: str | None = None
    phone_number: str | None = None
    email: EmailStr
    password: str
    parent_email: EmailStr | None = None


class Tutor_Request(BaseModel):
    fisrt_name: str | None = None
    second_name: str | None = None
    phone_number: str | None = None
    email: EmailStr
    password: str
