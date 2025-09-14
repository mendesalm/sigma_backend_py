# backend_python/schemas/permission_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PermissionBase(BaseModel):
    action: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=255)

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    action: Optional[str] = Field(None, min_length=3, max_length=255)

class PermissionResponse(PermissionBase):
    id: int
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        from_attributes = True # Permite que o modelo seja criado a partir de atributos de objeto (ORM)
