# backend_python/services/historico_cargo_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.models import HistoricoCargo, Cargo
from schemas.historico_cargo_schema import HistoricoCargoCreate, HistoricoCargoUpdate
from . import membro_service # Importa o serviço de membro para validação


def _get_cargo_by_id(db: Session, cargo_id: int) -> Cargo:
    """Função utilitária para buscar um cargo pelo ID."""
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not cargo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cargo com id {cargo_id} não encontrado.")
    return cargo

def create_historico_cargo(db: Session, historico_data: HistoricoCargoCreate) -> HistoricoCargo:
    """Cria um novo registro no histórico de cargos de um membro."""
    # Valida se o membro e o cargo existem
    membro_service.get_membro_by_id(db, historico_data.id_membro)
    _get_cargo_by_id(db, historico_data.id_cargo)

    novo_historico = HistoricoCargo(**historico_data.model_dump())
    db.add(novo_historico)
    db.commit()
    db.refresh(novo_historico)
    return novo_historico

def get_historico_by_id(db: Session, historico_id: int) -> HistoricoCargo:
    """Busca um registro de histórico de cargo pelo seu ID."""
    historico = db.query(HistoricoCargo).filter(HistoricoCargo.id == historico_id).first()
    if not historico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de histórico não encontrado.")
    return historico

def get_all_historico_from_membro(db: Session, membro_id: int):
    """Lista todo o histórico de cargos de um membro específico."""
    return db.query(HistoricoCargo).filter(HistoricoCargo.id_membro == membro_id).all()

def update_historico_cargo(db: Session, historico_id: int, historico_data: HistoricoCargoUpdate) -> HistoricoCargo:
    """Atualiza os dados de um registro de histórico de cargo."""
    db_historico = get_historico_by_id(db, historico_id)

    update_data = historico_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_historico, key, value)

    db.commit()
    db.refresh(db_historico)
    return db_historico

def delete_historico_cargo(db: Session, historico_id: int):
    """Deleta um registro de histórico de cargo do banco de dados."""
    db_historico = get_historico_by_id(db, historico_id)
    db.delete(db_historico)
    db.commit()
    return {"ok": True}
