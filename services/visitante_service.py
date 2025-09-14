# backend_python/services/visitante_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.models import Visitante
from schemas.visitante_schema import VisitanteCreate, VisitanteUpdate
from . import loja_externa_service # Importa o serviço de loja externa para validação

def create_visitante(db: Session, visitante_data: VisitanteCreate) -> Visitante:
    """Cria um novo visitante no banco de dados."""
    # Valida se a loja de origem externa existe, se fornecida
    if visitante_data.id_loja_origem:
        loja_externa_service.get_loja_externa_by_id(db, visitante_data.id_loja_origem)

    # Valida se o email já está em uso, se fornecido
    if visitante_data.email:
        db_visitante = db.query(Visitante).filter(Visitante.email == visitante_data.email).first()
        if db_visitante:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email de visitante já cadastrado.")

    novo_visitante = Visitante(**visitante_data.model_dump())
    db.add(novo_visitante)
    db.commit()
    db.refresh(novo_visitante)
    return novo_visitante

def get_visitante_by_id(db: Session, visitante_id: int) -> Visitante:
    """Busca um visitante pelo seu ID."""
    visitante = db.query(Visitante).filter(Visitante.id == visitante_id).first()
    if not visitante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitante não encontrado.")
    return visitante

def get_all_visitantes(db: Session, skip: int = 0, limit: int = 100):
    """Lista todos os visitantes."""
    return db.query(Visitante).offset(skip).limit(limit).all()

def update_visitante(db: Session, visitante_id: int, visitante_data: VisitanteUpdate) -> Visitante:
    """Atualiza os dados de um visitante."""
    db_visitante = get_visitante_by_id(db, visitante_id)

    update_data = visitante_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_visitante, key, value)

    db.commit()
    db.refresh(db_visitante)
    return db_visitante

def delete_visitante(db: Session, visitante_id: int):
    """Deleta um visitante do banco de dados."""
    db_visitante = get_visitante_by_id(db, visitante_id)
    db.delete(db_visitante)
    db.commit()
    return {"ok": True}
