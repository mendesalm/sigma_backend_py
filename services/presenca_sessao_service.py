# backend_python/services/presenca_sessao_service.py

from sqlalchemy.orm import Session
from models import models
from schemas import presenca_sessao_schema

def get_presencas_sessao(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PresencaSessao).offset(skip).limit(limit).all()

def get_presenca_sessao(db: Session, presenca_sessao_id: int):
    return db.query(models.PresencaSessao).filter(models.PresencaSessao.id == presenca_sessao_id).first()

def create_presenca_sessao(db: Session, presenca_sessao: presenca_sessao_schema.PresencaSessaoCreate):
    db_presenca_sessao = models.PresencaSessao(**presenca_sessao.dict())
    db.add(db_presenca_sessao)
    db.commit()
    db.refresh(db_presenca_sessao)
    return db_presenca_sessao