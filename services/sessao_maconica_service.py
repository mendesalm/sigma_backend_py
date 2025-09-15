# backend_python/services/sessao_maconica_service.py

from sqlalchemy.orm import Session
from models import models
from schemas import sessao_maconica_schema, presenca_sessao_schema

def get_sessoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SessaoMaconica).offset(skip).limit(limit).all()

def get_sessao(db: Session, sessao_id: int):
    return db.query(models.SessaoMaconica).filter(models.SessaoMaconica.id == sessao_id).first()

def create_sessao(db: Session, sessao: sessao_maconica_schema.SessaoMaconicaCreate, loja_id: int):
    db_sessao = models.SessaoMaconica(**sessao.dict(), id_loja=loja_id)
    db.add(db_sessao)
    db.commit()
    db.refresh(db_sessao)

    membros_ativos = db.query(models.MembroLoja).filter(models.MembroLoja.id_loja == loja_id, models.MembroLoja.situacao == 'Ativo').all()
    for membro in membros_ativos:
        presenca = presenca_sessao_schema.PresencaSessaoCreate(id_sessao=db_sessao.id, id_membro=membro.id, status_presenca='Ausente')
        db_presenca = models.PresencaSessao(**presenca.dict())
        db.add(db_presenca)
    
    db.commit()
    db.refresh(db_sessao)

    return db_sessao
