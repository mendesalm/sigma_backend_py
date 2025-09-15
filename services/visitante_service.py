# backend_python/services/visitante_service.py

from sqlalchemy.orm import Session
from models import models
from schemas import visitante_schema

def get_visitantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visitante).offset(skip).limit(limit).all()

def get_visitante(db: Session, visitante_id: int):
    return db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()

def create_visitante(db: Session, visitante: visitante_schema.VisitanteCreate):
    db_visitante = models.Visitante(**visitante.dict())
    db.add(db_visitante)
    db.commit()
    db.refresh(db_visitante)
    return db_visitante