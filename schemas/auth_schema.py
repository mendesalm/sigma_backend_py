# backend_python/schemas/auth_schema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LodgeMemberLogin(BaseModel):
    email: EmailStr
    senha: str

class LodgeMemberSelectLodge(BaseModel):
    lodge_id: int = Field(..., description="ID da loja a ser selecionada.")

class LodgeMemberForgotPassword(BaseModel):
    email: EmailStr

class LodgeMemberResetPassword(BaseModel):
    token: str
    nova_senha: str = Field(..., min_length=8)

class LodgeMemberAuthResponse(BaseModel):
    token_de_acesso: str
    tipo_token: str = "bearer"
    usuario: dict # Pode ser mais detalhado depois
