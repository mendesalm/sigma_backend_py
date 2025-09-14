# backend_python/schemas/sessao_maconica_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Enum para os tipos de sessão
class TipoSessao(str, Enum):
    ORDINARIA = "Ordinária"
    MAGNA = "Magna"
    EXTRAORDINARIA = "Extraordinária"

# Enum para os subtipos de sessão (exemplo, pode ser expandido)
class SubtipoSessaoOrdinaria(str, Enum):
    REGULAR = "Regular"
    INSTRUCAO = "Instrução"
    ADMINISTRATIVA = "Administrativa"
    FINANCAS = "Finanças"
    FILIACAO_REGULARIZACAO = "Filiação/Regularização"
    ELEITORAL = "Eleitoral"
    BANQUETE_RITUALISTICO = "Banquete Ritualístico"

class SubtipoSessaoMagna(str, Enum):
    INICIACAO = "Iniciação"
    ELEVACAO = "Elevação"
    EXALTACAO = "Exaltação"
    POSSE = "Posse"
    INSTALACAO = "Instalação"
    SAGRACAO_ESTANDARTE = "Sagração de Estandarte"
    REGULARIZACAO_LOJA = "Regularização de Loja"
    SAGRACAO_TEMPLO = "Sagração de Templo"
    ADOCAO_LOWTONS = "Adoção de Lowtons"
    CONSAGRACAO_MATRIMONIAL = "Consagração Matrimonial"
    EXALTACAO_MATRIMONIAL = "Exaltação Matrimonial"
    POMPAS_FUNEBRES = "Pompas Fúnebres"
    CONFERENCIA = "Conferência"
    PALESTRA = "Palestra"
    FESTIVA = "Festiva"
    CIVICO_CULTURAL = "Cívico-cultural"

class SubtipoSessaoExtraordinaria(str, Enum):
    ELEITORAL_GRAO_MESTRE_GERAL = "Eleitoral de Grão-Mestre Geral"
    ELEITORAL_GRAO_MESTRE_ADJUNTO = "Eleitoral de Grão-Mestre Adjunto"
    ELEITORAL_GRAO_MESTRE_ESTADUAL = "Eleitoral de Grão-Mestre Estadual"
    CONSELHO_FAMILIA = "Conselho de Família"
    CONCESSAO_PLACET_EX_OFFICIO = "Concessão de placet ex-officio"
    ALTERACAO_ESTATUTOS = "Alteração de estatutos"
    MUDANCA_RITO = "Mudança de Rito"
    MUDANCA_ORIENTE = "Mudança de Oriente"
    MUDANCA_TITULO_DISTINTIVO = "Mudança de Título Distintivo"
    FUSAO_INCORPORACAO_LOJAS = "Fusão ou incorporação de Lojas"

# Enum para o status da sessão
class StatusSessao(str, Enum):
    AGENDADA = "Agendada"
    EM_ANDAMENTO = "Em Andamento"
    REALIZADA = "Realizada"
    CANCELADA = "Cancelada"

# Schema base com campos comuns da Sessão Maçônica
class SessaoMaconicaBase(BaseModel):
    data_hora_inicio: datetime = Field(..., description="Data e hora de início da sessão.")
    tipo: TipoSessao = Field(..., description="Tipo da sessão (Ordinária, Magna, Extraordinária).")
    subtipo: str = Field(..., max_length=255, description="Subtipo da sessão.")
    status: StatusSessao = Field(StatusSessao.AGENDADA, description="Status atual da sessão.")

# Schema para criação de uma nova Sessão Maçônica
class SessaoMaconicaCreate(SessaoMaconicaBase):
    id_loja: int = Field(..., description="ID da loja à qual a sessão pertence.")

# Schema para atualização de uma Sessão Maçônica (todos os campos são opcionais)
class SessaoMaconicaUpdate(SessaoMaconicaBase):
    data_hora_inicio: Optional[datetime] = None
    tipo: Optional[TipoSessao] = None
    subtipo: Optional[str] = Field(None, max_length=255)
    status: Optional[StatusSessao] = None

# Schema para atualização de status específico
class SessaoMaconicaUpdateStatus(BaseModel):
    status: StatusSessao = Field(..., description="Novo status da sessão.")

# Schema para resposta da API (inclui campos gerados pelo banco de dados)
class SessaoMaconicaResponse(SessaoMaconicaBase):
    id: int
    id_loja: int
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        from_attributes = True
