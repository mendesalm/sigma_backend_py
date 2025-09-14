# backend_python/schemas/webmaster_schema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class WebmasterUpdateEmail(BaseModel):
    email: EmailStr = Field(..., description="Novo email para o webmaster.")

class WebmasterResetPasswordResponse(BaseModel):
    message: str
    new_password: str = Field(..., description="Nova senha gerada para o webmaster.")
