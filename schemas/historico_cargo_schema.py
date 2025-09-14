# backend_python/schemas/historico_cargo_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Schema aninhado para representar o Cargo na resposta
class CargoSimplesResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

# Schema base com campos comuns
class HistoricoCargoBase(BaseModel):
    id_cargo: int = Field(..., description="ID do cargo ocupado.")
    data_inicio: date = Field(..., description="Data de início no cargo.")
    data_termino: Optional[date] = Field(None, description="Data de término no cargo (se aplicável).")

# Schema para criação (requer o ID do membro)
class HistoricoCargoCreate(HistoricoCargoBase):
    id_membro: int = Field(..., description="ID do membro associado a este histórico.")

# Schema para atualização (apenas datas são atualizáveis)
class HistoricoCargoUpdate(BaseModel):
    data_inicio: Optional[date] = None
    data_termino: Optional[date] = None

# Schema para resposta da API (inclui o objeto do cargo)
class HistoricoCargoResponse(HistoricoCargoBase):
    id: int
    cargo: CargoSimplesResponse # Resposta aninhada com o nome do cargo

    class Config:
        from_attributes = True
