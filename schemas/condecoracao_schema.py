# backend_python/schemas/condecoracao_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Schema base com campos comuns
class CondecoracaoBase(BaseModel):
    titulo: str = Field(..., max_length=255, description="Título da condecoração ou honraria.")
    data_recebimento: date = Field(..., description="Data em que a condecoração foi recebida.")
    observacoes: Optional[str] = Field(None, description="Observações ou detalhes adicionais.")

# Schema para criação (requer o ID do membro)
class CondecoracaoCreate(CondecoracaoBase):
    id_membro: int = Field(..., description="ID do membro que recebeu a condecoração.")

# Schema para atualização (todos os campos são opcionais)
class CondecoracaoUpdate(CondecoracaoBase):
    titulo: Optional[str] = Field(None, max_length=255)
    data_recebimento: Optional[date] = None

# Schema para resposta da API
class CondecoracaoResponse(CondecoracaoBase):
    id: int

    class Config:
        from_attributes = True
