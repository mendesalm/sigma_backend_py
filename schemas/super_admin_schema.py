# backend_python/schemas/super_admin_schema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class SuperAdminBase(BaseModel):
    email: EmailStr

class SuperAdminCreate(SuperAdminBase):
    nome_usuario: str = Field(..., min_length=3, max_length=255)
    senha: str = Field(..., min_length=8, max_length=255)

class SuperAdminLogin(SuperAdminBase):
    senha: str

class SuperAdminUpdate(SuperAdminBase):
    nome_usuario: Optional[str] = Field(None, min_length=3, max_length=255)
    senha: Optional[str] = Field(None, min_length=8, max_length=255)
    esta_ativo: Optional[bool] = None

class SuperAdminResponse(SuperAdminBase):
    id: int
    nome_usuario: str
    esta_ativo: bool
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        from_attributes = True # Permite que o modelo seja criado a partir de atributos de objeto (ORM)
