# backend_python/schemas/familiar_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Schema base com campos comuns
class FamiliarBase(BaseModel):
    nome_completo: str = Field(..., max_length=255, description="Nome completo do familiar.")
    parentesco: str = Field(..., description="Parentesco (ex: Cônjuge, Filho, Filha).")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento do familiar.")
    falecido: bool = Field(False, description="Indica se o familiar é falecido.")

# Schema para criação de um novo familiar (requer o ID do membro)
class FamiliarCreate(FamiliarBase):
    id_membro: int = Field(..., description="ID do membro da loja ao qual o familiar está associado.")

# Schema para atualização (todos os campos são opcionais)
class FamiliarUpdate(FamiliarBase):
    nome_completo: Optional[str] = Field(None, max_length=255)
    parentesco: Optional[str] = None
    falecido: Optional[bool] = None

# Schema para resposta da API (inclui campos gerados pelo banco de dados)
class FamiliarResponse(FamiliarBase):
    id: int

    class Config:
        from_attributes = True
