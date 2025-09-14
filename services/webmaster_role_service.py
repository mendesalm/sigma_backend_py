# backend_python/services/webmaster_role_service.py

from sqlalchemy.orm import Session
from models.models import AssociacaoMembroLoja, Cargo, MembroLoja
from schemas.webmaster_role_schema import WebmasterRoleAssignment
from fastapi import HTTPException, status

def atribuir_cargo_a_membro_loja(db: Session, associacao_id: int, role_id: int):
    """Atribui um cargo a um membro da loja através de sua associação."""
    associacao = db.query(AssociacaoMembroLoja).filter(AssociacaoMembroLoja.id == associacao_id).first()
    if not associacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação de membro da loja não encontrada.")

    cargo = db.query(Cargo).filter(Cargo.id == role_id).first()
    if not cargo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cargo não encontrado.")

    associacao.role_id = role_id
    db.add(associacao)
    db.commit()
    db.refresh(associacao)
    return associacao

def remover_cargo_de_membro_loja(db: Session, associacao_id: int):
    """Remove o cargo de um membro da loja (definindo role_id como nulo, se permitido pelo schema)."""
    # Dependendo do schema, pode-se definir role_id como NULL ou remover a associação
    # Por simplicidade, vamos definir como NULL se o campo permitir, ou levantar erro
    associacao = db.query(AssociacaoMembroLoja).filter(AssociacaoMembroLoja.id == associacao_id).first()
    if not associacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação de membro da loja não encontrada.")
    
    # Se o role_id não puder ser nulo, esta operação pode precisar de mais lógica
    # ou ser uma exclusão da associação
    associacao.role_id = None # Assumindo que role_id pode ser nulo
    db.add(associacao)
    db.commit()
    db.refresh(associacao)
    return associacao

def obter_cargo_membro_loja(db: Session, associacao_id: int):
    """Obtém o cargo de um membro da loja através de sua associação."""
    associacao = db.query(AssociacaoMembroLoja).filter(AssociacaoMembroLoja.id == associacao_id).first()
    if not associacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação de membro da loja não encontrada.")
    
    db.refresh(associacao, attribute_names=['role'])
    return {
        "lodge_member_association_id": associacao.id,
        "role_id": associacao.role_id,
        "role_name": associacao.role.name if associacao.role else None
    }
