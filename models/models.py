# backend_python/models/models.py

from sqlalchemy import (Column, Integer, String, Boolean, DateTime, Enum, Time, 
                        Text, ForeignKey, func)
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
    responsavel_tecnico = relationship("MembroLoja", foreign_keys=[responsavel_tecnico_id])

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
    # Adicione outros campos de membro aqui (nome, email, etc.)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    loja = relationship("Loja", backref="membros")

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
