# backend_python/services/loja_externa_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.models import LojaExterna
from schemas.loja_externa_schema import LojaExternaCreate, LojaExternaUpdate

def create_loja_externa(db: Session, loja_externa_data: LojaExternaCreate) -> LojaExterna:
    """Cria uma nova loja externa no banco de dados."""
    # Valida se o nome da loja já existe
    db_loja_externa = db.query(LojaExterna).filter(LojaExterna.nome_loja == loja_externa_data.nome_loja).first()
    if db_loja_externa:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nome da loja externa já cadastrado.")

    nova_loja_externa = LojaExterna(**loja_externa_data.model_dump())
    db.add(nova_loja_externa)
    db.commit()
    db.refresh(nova_loja_externa)
    return nova_loja_externa

def get_loja_externa_by_id(db: Session, loja_externa_id: int) -> LojaExterna:
    """Busca uma loja externa pelo seu ID."""
    loja_externa = db.query(LojaExterna).filter(LojaExterna.id == loja_externa_id).first()
    if not loja_externa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja externa não encontrada.")
    return loja_externa

def get_all_lojas_externas(db: Session, skip: int = 0, limit: int = 100):
    """Lista todas as lojas externas."""
    return db.query(LojaExterna).offset(skip).limit(limit).all()

def update_loja_externa(db: Session, loja_externa_id: int, loja_externa_data: LojaExternaUpdate) -> LojaExterna:
    """Atualiza os dados de uma loja externa."""
    db_loja_externa = get_loja_externa_by_id(db, loja_externa_id)

    update_data = loja_externa_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_loja_externa, key, value)

    db.commit()
    db.refresh(db_loja_externa)
    return db_loja_externa

def delete_loja_externa(db: Session, loja_externa_id: int):
    """Deleta uma loja externa do banco de dados."""
    db_loja_externa = get_loja_externa_by_id(db, loja_externa_id)
    db.delete(db_loja_externa)
    db.commit()
    return {"ok": True}
