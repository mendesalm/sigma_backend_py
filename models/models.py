# backend_python/models/models.py

from sqlalchemy import (Column, Integer, String, Boolean, DateTime, Enum, Time, 
                        Text, ForeignKey, func, Date, CheckConstraint)
from sqlalchemy.orm import relationship
from database.connection import Base  # Importa a Base declarativa

# Modelo base para campos comuns de timestamp
class ModeloBase(Base):
    """Modelo abstrato com campos de data de criação e atualização."""
    __abstract__ = True

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

# --- Modelos SQLAlchemy ---

class SuperAdministrador(ModeloBase):
    __tablename__ = "super_administradores"

    id = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    esta_ativo = Column(Boolean, default=True)

class Classe(ModeloBase):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False)
    descricao = Column(String(255))

class Loja(ModeloBase):
    __tablename__ = "lojas"

    id = Column(Integer, primary_key=True, index=True)
    codigo_loja = Column(String(32), unique=True, index=True, nullable=False)
    numero_loja = Column(String(255))
    nome_loja = Column(String(255))
    titulo_loja = Column(String(255))
    obediencia_loja = Column(String(255))
    id_classe = Column(Integer, ForeignKey('classes.id'))
    responsavel_tecnico_id = Column(Integer, ForeignKey('membros_loja.id'), nullable=True)
    dominio_personalizado = Column(String(255), unique=True)
    plano = Column(String(255))
    limite_usuarios = Column(Integer)
    configuracoes_globais = Column(Text)  # Pode ser um JSON como string
    chaves_api = Column(Text)  # Pode ser um JSON como string
    esta_ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(255))
    dia_sessoes = Column(Enum('Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', name='dia_sessoes_enum'))
    periodicidade = Column(Enum('Semanal', 'Quinzenal', 'Mensal', name='periodicidade_enum'))
    hora_sessao = Column(Time)

    classe = relationship("Classe", backref="lojas")
    responsavel_tecnico = relationship("MembroLoja", foreign_keys=[responsavel_tecnico_id], post_update=True)

class Webmaster(ModeloBase):
    __tablename__ = "webmasters"

    id = Column(Integer, primary_key=True, index=True)
    id_loja = Column(Integer, ForeignKey('lojas.id'))
    nome_usuario = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    esta_ativo = Column(Boolean, default=True)

    loja = relationship("Loja", backref="webmasters")

class Permissao(ModeloBase):
    __tablename__ = "permissoes"

    id = Column(Integer, primary_key=True, index=True)
    acao = Column(String(255), unique=True, nullable=False)
    descricao = Column(String(255))

class Cargo(ModeloBase):
    __tablename__ = "cargos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False)
    id_classe = Column(Integer, ForeignKey('classes.id'))

    classe = relationship("Classe", backref="cargos")

class CargoPermissao(ModeloBase):
    __tablename__ = "cargos_permissoes"

    id_cargo = Column(Integer, ForeignKey('cargos.id'), primary_key=True)
    id_permissao = Column(Integer, ForeignKey('permissoes.id'), primary_key=True)

    cargo = relationship("Cargo", backref="permissoes_associadas")
    permissao = relationship("Permissao", backref="cargos_associados")

class HierarquiaLoja(ModeloBase):
    __tablename__ = "hierarquia_lojas"

    id = Column(Integer, primary_key=True, index=True)
    id_loja_superior = Column(Integer, ForeignKey('lojas.id'), nullable=False)
    id_loja_subordinada = Column(Integer, ForeignKey('lojas.id'), nullable=False)
    tipo_relacionamento = Column(Enum('jurisdicionada', 'federada', 'subordinada', name='relationship_type_enum'), nullable=False)

    loja_superior = relationship("Loja", foreign_keys=[id_loja_superior], backref="subordinadas")
    loja_subordinada = relationship("Loja", foreign_keys=[id_loja_subordinada], backref="superiores")

class MembroLoja(ModeloBase):
    __tablename__ = "membros_loja"

    id = Column(Integer, primary_key=True, index=True)
    id_loja = Column(Integer, ForeignKey('lojas.id'), nullable=False)

    # Campos de Autenticação
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=True)  # Nulável para membros que não são usuários
    email_verification_token = Column(String(255), nullable=True)
    email_verification_expires = Column(DateTime(timezone=True), nullable=True)
    reset_password_token = Column(String(255), nullable=True)
    reset_password_expires = Column(DateTime(timezone=True), nullable=True)
    ultimo_login = Column(DateTime(timezone=True), nullable=True)

    # Dados Pessoais
    nome_completo = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=True)
    cim = Column(String(20), unique=True, nullable=True)  # Carteira de Identidade Maçônica
    identidade = Column(String(100), nullable=True)
    foto_pessoal_caminho = Column(String(255), nullable=True)
    data_nascimento = Column(Date, nullable=True)
    data_casamento = Column(Date, nullable=True)
    naturalidade = Column(String(100), nullable=True)
    nacionalidade = Column(String(100), nullable=True)
    religiao = Column(String(100), nullable=True)
    nome_pai = Column(String(255), nullable=True)
    nome_mae = Column(String(255), nullable=True)

    # Formação e Ocupação
    formacao_academica = Column(String(255), nullable=True)
    ocupacao = Column(String(255), nullable=True)
    local_trabalho = Column(String(255), nullable=True)

    # Contato
    telefone = Column(String(20), nullable=True)
    endereco_rua = Column(String(255), nullable=True)
    endereco_numero = Column(String(20), nullable=True)
    endereco_bairro = Column(String(100), nullable=True)
    endereco_cidade = Column(String(100), nullable=True)
    endereco_cep = Column(String(10), nullable=True)

    # Dados Maçônicos
    situacao = Column(String(50), default='Ativo')
    graduacao = Column(Enum('Aprendiz', 'Companheiro', 'Mestre', 'Mestre Instalado', name='graduacao_enum'), nullable=True)
    grau_filosofico = Column(String(100), nullable=True)
    data_iniciacao = Column(Date, nullable=True)
    data_elevacao = Column(Date, nullable=True)
    data_exaltacao = Column(Date, nullable=True)
    data_filiacao = Column(Date, nullable=True)
    data_regularizacao = Column(Date, nullable=True)
    status_cadastro = Column(Enum("Pendente", "Aprovado", "Rejeitado", "VerificacaoEmailPendente", name='status_cadastro_enum'), nullable=False, default="Pendente")

    # Relacionamentos
    loja = relationship("Loja", backref="membros", foreign_keys=[id_loja])
    familiares = relationship("Familiar", backref="membro", cascade="all, delete-orphan")
    condecoracoes = relationship("Condecoracao", backref="membro", cascade="all, delete-orphan")
    historico_cargos = relationship("HistoricoCargo", backref="membro", cascade="all, delete-orphan")
    presencas = relationship("PresencaSessao", backref="membro")

class Familiar(ModeloBase):
    __tablename__ = "familiares"

    id = Column(Integer, primary_key=True, index=True)
    id_membro = Column(Integer, ForeignKey('membros_loja.id'), nullable=False)
    nome_completo = Column(String(255), nullable=False)
    parentesco = Column(Enum('Cônjuge', 'Filho', 'Filha', name='parentesco_enum'), nullable=False)
    data_nascimento = Column(Date, nullable=True)
    email = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=True)
    falecido = Column(Boolean, default=False, nullable=False)

class Condecoracao(ModeloBase):
    __tablename__ = "condecoracoes"

    id = Column(Integer, primary_key=True, index=True)
    id_membro = Column(Integer, ForeignKey('membros_loja.id'), nullable=False)
    titulo = Column(String(255), nullable=False)
    data_recebimento = Column(Date, nullable=False)
    observacoes = Column(Text, nullable=True)

class HistoricoCargo(ModeloBase):
    __tablename__ = "historico_cargos"

    id = Column(Integer, primary_key=True, index=True)
    id_membro = Column(Integer, ForeignKey('membros_loja.id'), nullable=False)
    id_cargo = Column(Integer, ForeignKey('cargos.id'), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_termino = Column(Date, nullable=True)

    cargo = relationship("Cargo")

class AssociacaoMembroLoja(ModeloBase):
    __tablename__ = "associacoes_membros_loja"

    id = Column(Integer, primary_key=True, index=True)
    id_membro_loja = Column(Integer, ForeignKey('membros_loja.id'), nullable=False)
    id_cargo = Column(Integer, ForeignKey('cargos.id'), nullable=False)

    membro_loja = relationship("MembroLoja", backref="associacoes")
    cargo = relationship("Cargo", backref="associacoes_membros")

class ProcessoAdministrativo(ModeloBase):
    __tablename__ = "processos_administrativos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text)
    status = Column(String(50), nullable=False)
    id_loja = Column(Integer, ForeignKey('lojas.id'), nullable=False)

    loja = relationship("Loja", backref="processos_administrativos")

# Modelos para Gestão de Sessões Maçônicas

class SessaoMaconica(ModeloBase):
    __tablename__ = "sessoes_maconicas"

    id = Column(Integer, primary_key=True, index=True)
    id_loja = Column(Integer, ForeignKey('lojas.id'), nullable=False)
    data_sessao = Column(DateTime(timezone=True), nullable=False)
    tipo = Column(Enum('Ordinária', 'Magna', 'Extraordinária', name='tipo_sessao_enum'), nullable=False)
    subtipo = Column(String(255), nullable=True)
    status = Column(Enum('Agendada', 'Em Andamento', 'Realizada', 'Cancelada', name='status_sessao_enum'), nullable=False, default='Agendada')

    loja = relationship("Loja", backref="sessoes")
    presencas = relationship("PresencaSessao", backref="sessao")
    visitantes = relationship("Visitante", backref="sessao")

class PresencaSessao(ModeloBase):
    __tablename__ = "presencas_sessao"

    id = Column(Integer, primary_key=True, index=True)
    id_sessao = Column(Integer, ForeignKey('sessoes_maconicas.id'), nullable=False)
    id_membro = Column(Integer, ForeignKey('membros_loja.id'), nullable=False)
    status_presenca = Column(Enum('Presente', 'Justificado', 'Ausente', name='status_presenca_enum'), nullable=False, default='Ausente')

class LojaExterna(ModeloBase):
    __tablename__ = "lojas_externas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    numero = Column(Integer, nullable=True)
    obediencia = Column(String(255), nullable=True)

class Visitante(ModeloBase):
    __tablename__ = "visitantes"

    id = Column(Integer, primary_key=True, index=True)
    id_sessao = Column(Integer, ForeignKey('sessoes_maconicas.id'), nullable=False)
    nome_completo = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=True)
    id_loja_externa = Column(Integer, ForeignKey('lojas_externas.id'), nullable=True)

    loja_externa = relationship("LojaExterna", backref="visitantes")
