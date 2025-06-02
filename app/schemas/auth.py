from pydantic import BaseModel, EmailStr 
from typing import Optional


class UserSignup(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    token_type: str = "bearer" 
    expires_in: Optional[int] = None