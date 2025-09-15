# backend_python/services/loja_externa_service.py

from sqlalchemy.orm import Session
from models import models
from schemas import loja_externa_schema

def get_lojas_externas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LojaExterna).offset(skip).limit(limit).all()

def get_loja_externa(db: Session, loja_externa_id: int):
    return db.query(models.LojaExterna).filter(models.LojaExterna.id == loja_externa_id).first()

def create_loja_externa(db: Session, loja_externa: loja_externa_schema.LojaExternaCreate):
    db_loja_externa = models.LojaExterna(**loja_externa.dict())
    db.add(db_loja_externa)
    db.commit()
    db.refresh(db_loja_externa)
    return db_loja_externa