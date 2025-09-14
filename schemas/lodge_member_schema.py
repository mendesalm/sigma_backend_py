# backend_python/schemas/lodge_member_schema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class LodgeMemberBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    # Adicionar outros campos do membro conforme o modelo MembroLoja

class LodgeMemberCreate(LodgeMemberBase):
    senha: str = Field(..., min_length=8)
    tenant_id: int = Field(..., description="ID da loja a que o membro pertence.")
    role_id: int = Field(..., description="ID do cargo a ser atribuído ao membro.")

class LodgeMemberUpdate(LodgeMemberBase):
    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(None, min_length=8)
    role_id: Optional[int] = Field(None, description="Novo ID do cargo do membro.")

class LodgeMemberResponse(LodgeMemberBase):
    id: int
    tenant_id: int
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        from_attributes = True # Permite que o modelo seja criado a partir de atributos de objeto (ORM)
