# backend_python/services/role_permission_service.py

from sqlalchemy.orm import Session
from models.models import CargoPermissao, Cargo, Permissao
from schemas.role_permission_schema import RolePermissionCreate
from fastapi import HTTPException, status

def atribuir_permissao_a_cargo(db: Session, role_id: int, permission_id: int):
    """Atribui uma permissão a um cargo."""
    # Verifica se o cargo e a permissão existem
    cargo = db.query(Cargo).filter(Cargo.id == role_id).first()
    permissao = db.query(Permissao).filter(Permissao.id == permission_id).first()

    if not cargo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cargo não encontrado.")
    if not permissao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissão não encontrada.")

    # Verifica se a associação já existe
    associacao_existente = db.query(CargoPermissao).filter(
        CargoPermissao.role_id == role_id,
        CargoPermissao.permission_id == permission_id
    ).first()

    if associacao_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Permissão já atribuída a este cargo.")

    nova_associacao = CargoPermissao(role_id=role_id, permission_id=permission_id)
    db.add(nova_associacao)
    db.commit()
    db.refresh(nova_associacao)
    return nova_associacao

def remover_permissao_de_cargo(db: Session, role_id: int, permission_id: int):
    """Remove uma permissão de um cargo."""
    associacao = db.query(CargoPermissao).filter(
        CargoPermissao.role_id == role_id,
        CargoPermissao.permission_id == permission_id
    ).first()

    if not associacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação não encontrada.")

    db.delete(associacao)
    db.commit()
    return {"mensagem": "Permissão removida do cargo com sucesso."}

def obter_permissoes_por_cargo(db: Session, role_id: int):
    """Retorna todas as permissões associadas a um cargo."""
    cargo = db.query(Cargo).filter(Cargo.id == role_id).first()
    if not cargo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cargo não encontrado.")
    
    # Carrega as permissões através do relacionamento
    return [associacao.permission for associacao in cargo.permissoes_associadas]

def obter_cargos_por_permissao(db: Session, permission_id: int):
    """Retorna todos os cargos que possuem uma permissão específica."""
    permissao = db.query(Permissao).filter(Permissao.id == permission_id).first()
    if not permissao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissão não encontrada.")

    # Carrega os cargos através do relacionamento
    return [associacao.role for associacao in permissao.cargos_associados]
