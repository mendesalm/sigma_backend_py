# backend_python/services/potencia_service.py
from sqlalchemy.orm import Session
from models.models import Potencia
from schemas.potencia_schema import PotenciaCreate, PotenciaUpdate
from fastapi import HTTPException, status

def create_potencia(db: Session, potencia: PotenciaCreate) -> Potencia:
    db_potencia = db.query(Potencia).filter(Potencia.nome == potencia.nome).first()
    if db_potencia:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Uma potência com este nome já existe.")
    new_potencia = Potencia(**potencia.model_dump())
    db.add(new_potencia)
    db.commit()
    db.refresh(new_potencia)
    return new_potencia

# ... (get_potencia, get_all_potencias, update_potencia, delete_potencia)
