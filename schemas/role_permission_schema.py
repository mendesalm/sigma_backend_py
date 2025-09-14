# backend_python/schemas/role_permission_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RolePermissionBase(BaseModel):
    role_id: int = Field(..., description="ID do cargo.")
    permission_id: int = Field(..., description="ID da permissão.")

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermissionResponse(RolePermissionBase):
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        from_attributes = True # Permite que o modelo seja criado a partir de atributos de objeto (ORM)
