# backend_python/schemas/role_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RoleBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    lodge_class_id: Optional[int] = Field(None, description="ID da classe de loja a que este cargo pertence.")

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    name: Optional[str] = Field(None, min_length=3, max_length=255)

class RoleResponse(RoleBase):
    id: int
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        from_attributes = True # Permite que o modelo seja criado a partir de atributos de objeto (ORM)
