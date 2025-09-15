# backend_python/schemas/sessao_maconica_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class PresencaSessaoBase(BaseModel):
    id_membro: int
    status_presenca: str

class PresencaSessaoCreate(PresencaSessaoBase):
    pass

class PresencaSessao(PresencaSessaoBase):
    id: int
    id_sessao: int

    class Config:
        orm_mode = True

class VisitanteBase(BaseModel):
    nome_completo: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    id_loja_externa: Optional[int] = None

class VisitanteCreate(VisitanteBase):
    pass

class Visitante(VisitanteBase):
    id: int
    id_sessao: int

    class Config:
        orm_mode = True

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
    visitantes: List[Visitante] = []

    class Config:
        orm_mode = True