# backend_python/schemas/membro_schema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime

from .familiar_schema import FamiliarResponse
from .condecoracao_schema import CondecoracaoResponse
from .historico_cargo_schema import HistoricoCargoResponse

# Schema base com os campos principais do membro
class MembroBase(BaseModel):
    email: EmailStr = Field(..., description="Email do membro, usado para login.")
    nome_completo: str = Field(..., max_length=255)
    cpf: Optional[str] = Field(None, max_length=14, description="CPF do membro.")
    cim: Optional[str] = Field(None, max_length=20, description="Carteira de Identidade Maçônica.")
    data_nascimento: Optional[date] = None
    naturalidade: Optional[str] = Field(None, max_length=100)
    nacionalidade: Optional[str] = Field(None, max_length=100)
    telefone: Optional[str] = Field(None, max_length=20)
    endereco_rua: Optional[str] = Field(None, max_length=255)
    endereco_numero: Optional[str] = Field(None, max_length=20)
    endereco_bairro: Optional[str] = Field(None, max_length=100)
    endereco_cidade: Optional[str] = Field(None, max_length=100)
    endereco_cep: Optional[str] = Field(None, max_length=10)
    situacao: Optional[str] = Field('Ativo', max_length=50)
    graduacao: Optional[str] = Field(None, description="Grau do membro (Aprendiz, Companheiro, Mestre)")
    data_iniciacao: Optional[date] = None

# Schema para criação de um novo membro
class MembroCreate(MembroBase):
    senha: str = Field(..., min_length=8, description="Senha para o primeiro acesso do membro.")
    id_loja: int = Field(..., description="ID da loja à qual o membro será associado.")

# Schema para atualização de um membro (todos os campos são opcionais)
class MembroUpdate(MembroBase):
    email: Optional[EmailStr] = None
    nome_completo: Optional[str] = Field(None, max_length=255)
    senha: Optional[str] = Field(None, min_length=8, description="Nova senha (se for alterar).")

# Schema completo para resposta da API, incluindo relacionamentos
class MembroResponse(MembroBase):
    id: int
    id_loja: int
    criado_em: datetime
    atualizado_em: Optional[datetime] = None
    familiares: List[FamiliarResponse] = []
    condecoracoes: List[CondecoracaoResponse] = []
    historico_cargos: List[HistoricoCargoResponse] = []

    class Config:
        from_attributes = True
