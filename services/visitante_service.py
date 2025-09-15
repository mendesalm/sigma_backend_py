# backend_python/services/visitante_service.py

from sqlalchemy.orm import Session
from models import models
from schemas import visitante_schema

def get_visitantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visitante).offset(skip).limit(limit).all()

def get_visitante(db: Session, visitante_id: int):
    return db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()

def update_visitante(db: Session, visitante_id: int, visitante: visitante_schema.VisitanteCreate):
    db_visitante = get_visitante(db, visitante_id)
    if db_visitante:
        for key, value in visitante.dict().items():
            setattr(db_visitante, key, value)
        db.commit()
        db.refresh(db_visitante)
    return db_visitante

def delete_visitante(db: Session, visitante_id: int):
    db_visitante = get_visitante(db, visitante_id)
    if db_visitante:
        db.delete(db_visitante)
        db.commit()
    return db_visitante