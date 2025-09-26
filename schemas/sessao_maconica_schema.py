# backend_python/schemas/sessao_maconica_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from schemas.presenca_sessao_schema import PresencaSessao # Importa o modelo atualizado
from pydantic_settings import SettingsConfigDict

class SessaoMaconicaBase(BaseModel):
    data_sessao: datetime
    tipo: str
    subtipo: Optional[str] = None
    status: str

class SessaoMaconicaCreate(SessaoMaconicaBase):
    pass

class SessaoMaconicaUpdate(SessaoMaconicaBase):
    pass

class SessaoMaconica(SessaoMaconicaBase):
    id: int
    id_loja: int
    presencas: List[PresencaSessao] = []

    model_config = SettingsConfigDict(from_attributes=True)
