# backend_python/services/sessao_maconica_service.py

from sqlalchemy.orm import Session
from models import models
from schemas import sessao_maconica_schema

def get_sessoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SessaoMaconica).offset(skip).limit(limit).all()

def get_sessao(db: Session, sessao_id: int):
    return db.query(models.SessaoMaconica).filter(models.SessaoMaconica.id == sessao_id).first()

def create_sessao(db: Session, sessao: sessao_maconica_schema.SessaoMaconicaCreate, loja_id: int):
    db_sessao = models.SessaoMaconica(**sessao.dict(), id_loja=loja_id)
    db.add(db_sessao)
    db.commit()
    db.refresh(db_sessao)
    return db_sessao