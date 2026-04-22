from pydantic import BaseModel, EmailStr, Field


class SignupIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = Field(default="analyst", pattern="^(admin|analyst)$")


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AnalyzeIn(BaseModel):
    company_a_id: int
    target_company_id: int
