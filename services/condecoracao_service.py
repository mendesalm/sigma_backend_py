# backend_python/services/condecoracao_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.models import Condecoracao
from schemas.condecoracao_schema import CondecoracaoCreate, CondecoracaoUpdate
from . import membro_service # Importa o serviço de membro para validação

def create_condecoracao(db: Session, condecoracao_data: CondecoracaoCreate) -> Condecoracao:
    """Cria uma nova condecoração para um membro."""
    # Valida se o membro associado existe
    membro_service.get_membro_by_id(db, condecoracao_data.id_membro)

    nova_condecoracao = Condecoracao(**condecoracao_data.model_dump())
    db.add(nova_condecoracao)
    db.commit()
    db.refresh(nova_condecoracao)
    return nova_condecoracao

def get_condecoracao_by_id(db: Session, condecoracao_id: int) -> Condecoracao:
    """Busca uma condecoração pelo seu ID."""
    condecoracao = db.query(Condecoracao).filter(Condecoracao.id == condecoracao_id).first()
    if not condecoracao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Condecoração não encontrada.")
    return condecoracao

def get_all_condecoracoes_from_membro(db: Session, membro_id: int):
    """Lista todas as condecorações de um membro específico."""
    return db.query(Condecoracao).filter(Condecoracao.id_membro == membro_id).all()

def update_condecoracao(db: Session, condecoracao_id: int, condecoracao_data: CondecoracaoUpdate) -> Condecoracao:
    """Atualiza os dados de uma condecoração."""
    db_condecoracao = get_condecoracao_by_id(db, condecoracao_id)

    update_data = condecoracao_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_condecoracao, key, value)

    db.commit()
    db.refresh(db_condecoracao)
    return db_condecoracao

def delete_condecoracao(db: Session, condecoracao_id: int):
    """Deleta uma condecoração do banco de dados."""
    db_condecoracao = get_condecoracao_by_id(db, condecoracao_id)
    db.delete(db_condecoracao)
    db.commit()
    return {"ok": True}
