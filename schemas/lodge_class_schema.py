# backend_python/schemas/lodge_class_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LodgeClassBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    descricao: Optional[str] = Field(None, max_length=255)

class LodgeClassCreate(LodgeClassBase):
    pass

class LodgeClassUpdate(LodgeClassBase):
    nome: Optional[str] = Field(None, min_length=3, max_length=255)

class LodgeClassResponse(LodgeClassBase):
    id: int
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        from_attributes = True # Permite que o modelo seja criado a partir de atributos de objeto (ORM)
