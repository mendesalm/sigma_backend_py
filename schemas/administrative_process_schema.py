# backend_python/schemas/administrative_process_schema.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Assumindo uma estrutura simples para o processo administrativo
class AdministrativeProcessBase(BaseModel):
    titulo: str = Field(..., max_length=255)
    descricao: Optional[str] = None
    status: str = Field(..., max_length=50)
    loja_id: int = Field(..., description="ID da loja a que o processo pertence.")

class AdministrativeProcessCreate(AdministrativeProcessBase):
    pass

class AdministrativeProcessUpdate(AdministrativeProcessBase):
    titulo: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, max_length=50)

class AdministrativeProcessResponse(AdministrativeProcessBase):
    id: int
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        from_attributes = True # Permite que o modelo seja criado a partir de atributos de objeto (ORM)
