# backend_python/services/permission_service.py

from sqlalchemy.orm import Session
from models.models import Permission
from schemas.permission_schema import PermissionCreate, PermissionUpdate
from fastapi import HTTPException, status

def criar_permissao(db: Session, permissao: PermissionCreate):
    """Cria uma nova permissão no banco de dados."""
    db_permissao = Permission(action=permissao.action, description=permissao.description)
    db.add(db_permissao)
    db.commit()
    db.refresh(db_permissao)
    return db_permissao

def obter_todas_permissoes(db: Session):
    """Retorna todas as permissões do banco de dados."""
    return db.query(Permission).all()

def obter_permissao_por_id(db: Session, permissao_id: int):
    """Retorna uma permissão específica pelo ID."""
    permissao = db.query(Permission).filter(Permission.id == permissao_id).first()
    if not permissao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissão não encontrada.")
    return permissao

def atualizar_permissao(db: Session, permissao_id: int, permissao_atualizacao: PermissionUpdate):
    """Atualiza uma permissão existente no banco de dados."""
    db_permissao = obter_permissao_por_id(db, permissao_id)
    
    update_data = permissao_atualizacao.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_permissao, key, value)

    db.add(db_permissao)
    db.commit()
    db.refresh(db_permissao)
    return db_permissao

def deletar_permissao(db: Session, permissao_id: int):
    """Deleta uma permissão do banco de dados."""
    db_permissao = obter_permissao_por_id(db, permissao_id)
    db.delete(db_permissao)
    db.commit()
    return {"mensagem": "Permissão deletada com sucesso."}
