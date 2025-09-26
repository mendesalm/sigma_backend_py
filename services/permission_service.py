# backend_python/services/permission_service.py

from sqlalchemy.orm import Session
from models.models import Permissao
from schemas.permission_schema import PermissionCreate, PermissionUpdate
from fastapi import HTTPException, status

def criar_permissao(db: Session, permissao: PermissionCreate):
    """Cria uma nova permissão no banco de dados."""
    db_permissao = Permissao(acao=permissao.acao, descricao=permissao.descricao)
    db.add(db_permissao)
    db.commit()
    db.refresh(db_permissao)
    return db_permissao

def obter_todas_permissoes(db: Session):
    """Retorna todas as permissões do banco de dados."""
    return db.query(Permissao).all()

def obter_permissao_por_id(db: Session, permissao_id: int):
    """Retorna uma permissão específica pelo ID."""
    permissao = db.query(Permissao).filter(Permissao.id == permissao_id).first()
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

def ensure_session_permissions(db: Session):
    permissions_to_ensure = [
        {"acao": "sessao:criar", "descricao": "Permite agendar novas sessões."},
        {"acao": "sessao:gerenciar", "descricao": "Permite editar, cancelar ou deletar sessões."},
        {"acao": "sessao:gerenciar_presenca", "descricao": "Permite manipular a lista de presença manualmente."},
    ]

    for perm_data in permissions_to_ensure:
        existing_perm = db.query(Permissao).filter(Permissao.acao == perm_data["acao"]).first()
        if not existing_perm:
            new_perm = Permissao(acao=perm_data["acao"], descricao=perm_data["descricao"])
            db.add(new_perm)
            db.commit()
            db.refresh(new_perm)
            print(f"Permissão criada: {new_perm.acao}")
        else:
            print(f"Permissão já existe: {existing_perm.acao}")