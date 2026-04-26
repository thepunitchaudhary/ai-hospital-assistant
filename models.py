from pydantic import BaseModel, field_validator


class RegisterReq(BaseModel):
    full_name: str
    email:     str
    phone:     str = ""
    password:  str

    @field_validator("full_name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_valid(cls, v):
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email address")
        return v.lower().strip()

    @field_validator("password")
    @classmethod
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class LoginReq(BaseModel):
    email:    str
    password: str


class MessageReq(BaseModel):
    text:       str
    session_id: str        = "default"
    name:       str | None = None
    email:      str | None = None
    user_id:    int | None = None