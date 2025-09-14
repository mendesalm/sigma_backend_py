# backend_python/services/familiar_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.models import Familiar
from schemas.familiar_schema import FamiliarCreate, FamiliarUpdate
from . import membro_service # Importa o serviço de membro para validação

def create_familiar(db: Session, familiar_data: FamiliarCreate) -> Familiar:
    """Cria um novo familiar para um membro."""
    # Valida se o membro associado existe
    membro_service.get_membro_by_id(db, familiar_data.id_membro)

    novo_familiar = Familiar(**familiar_data.model_dump())
    db.add(novo_familiar)
    db.commit()
    db.refresh(novo_familiar)
    return novo_familiar

def get_familiar_by_id(db: Session, familiar_id: int) -> Familiar:
    """Busca um familiar pelo seu ID."""
    familiar = db.query(Familiar).filter(Familiar.id == familiar_id).first()
    if not familiar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Familiar não encontrado.")
    return familiar

def get_all_familiares_from_membro(db: Session, membro_id: int):
    """Lista todos os familiares de um membro específico."""
    return db.query(Familiar).filter(Familiar.id_membro == membro_id).all()

def update_familiar(db: Session, familiar_id: int, familiar_data: FamiliarUpdate) -> Familiar:
    """Atualiza os dados de um familiar."""
    db_familiar = get_familiar_by_id(db, familiar_id)

    update_data = familiar_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_familiar, key, value)

    db.commit()
    db.refresh(db_familiar)
    return db_familiar

def delete_familiar(db: Session, familiar_id: int):
    """Deleta um familiar do banco de dados."""
    db_familiar = get_familiar_by_id(db, familiar_id)
    db.delete(db_familiar)
    db.commit()
    return {"ok": True}
