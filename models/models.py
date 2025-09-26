# backend_python/models/models.py

from sqlalchemy import (Column, Integer, String, Boolean, DateTime, Enum as SQLAlchemyEnum, Time, 
                        Text, ForeignKey, func, Date, Table)
from sqlalchemy.orm import relationship
from database.connection import Base
import enum

class ModeloBase(Base):
    __abstract__ = True
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

# --- ENUMS ---
class TipoPotenciaEnum(str, enum.Enum):
    FEDERAL = "Federal"
    ESTADUAL = "Estadual"

class RitoEnum(str, enum.Enum):
    REAA = "REAA"
    YORK = "YORK"
    # ... (outros ritos)

# --- TABELAS DE ASSOCIAÇÃO ---
cargos_permissoes = Table(
    'cargos_permissoes',
    Base.metadata,
    Column('id_cargo', ForeignKey('cargos.id'), primary_key=True),
    Column('id_permissao', ForeignKey('permissoes.id'), primary_key=True)
)

# --- MODELOS PRINCIPAIS ---

class Potencia(ModeloBase):
    __tablename__ = "potencias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False)
    descricao = Column(String(255))
    tipo = Column(SQLAlchemyEnum(TipoPotenciaEnum), nullable=False)
    id_potencia_superior = Column(Integer, ForeignKey('potencias.id'), nullable=True)
    cnpj = Column(String(18), unique=True, nullable=True)
    email = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=True)
    site = Column(String(255), nullable=True)
    logradouro = Column(String(255), nullable=True)
    numero = Column(String(20), nullable=True)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    cep = Column(String(9), nullable=True)
    responsavel_tecnico_nome = Column(String(255), nullable=True)
    responsavel_tecnico_email = Column(String(255), nullable=True)
    potencia_superior = relationship("Potencia", remote_side=[id], backref="potencias_subordinadas")

class Loja(ModeloBase):
    __tablename__ = "lojas"
    id = Column(Integer, primary_key=True, index=True)
    nome_loja = Column(String(255), nullable=False)
    codigo_loja = Column(String(32), unique=True, index=True, nullable=False)
    numero_loja = Column(String(255))
    data_fundacao = Column(Date, nullable=True)
    rito = Column(SQLAlchemyEnum(RitoEnum), nullable=True)
    id_potencia = Column(Integer, ForeignKey('potencias.id'), nullable=False)
    obediencia_loja = Column(String(255))
    cnpj = Column(String(18), unique=True, nullable=True)
    email = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=True)
    site = Column(String(255), nullable=True)
    logradouro = Column(String(255), nullable=True)
    numero = Column(String(20), nullable=True)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    cep = Column(String(9), nullable=True)
    dominio_personalizado = Column(String(255), unique=True)
    plano = Column(String(255))
    limite_usuarios = Column(Integer)
    esta_ativo = Column(Boolean, default=True)
    status = Column(String(255))
    dia_sessoes = Column(SQLAlchemyEnum('Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', name='dia_sessoes_enum'))
    periodicidade = Column(SQLAlchemyEnum('Semanal', 'Quinzenal', 'Mensal', name='periodicidade_enum'))
    hora_sessao = Column(Time)
    potencia = relationship("Potencia", backref="lojas")

class Cargo(ModeloBase):
    __tablename__ = "cargos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False)
    id_potencia = Column(Integer, ForeignKey('potencias.id'))
    potencia = relationship("Potencia", backref="cargos")
    permissoes = relationship("Permissao", secondary=cargos_permissoes, back_populates="cargos")

class Permissao(ModeloBase):
    __tablename__ = "permissoes"
    id = Column(Integer, primary_key=True, index=True)
    acao = Column(String(255), unique=True, nullable=False)
    descricao = Column(String(255))
    cargos = relationship("Cargo", secondary=cargos_permissoes, back_populates="permissoes")

class SuperAdministrador(ModeloBase):
    __tablename__ = "super_administradores"
    id = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    esta_ativo = Column(Boolean, default=True)
