# backend_python/controllers/global/role_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.role_schema import RoleCreate, RoleUpdate, RoleResponse
from services import role_service
from middleware.authorize_middleware import get_current_user
from models.models import SuperAdministrador

router = APIRouter()

# Dependência para garantir que o usuário é um SuperAdmin
async def get_current_super_admin(current_user_data: dict = Depends(get_current_user)) -> SuperAdministrador:
    if current_user_data.get("perfil") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas Super Administradores podem realizar esta ação."
        )
    return current_user_data.get("user")

@router.post(
    "/", 
    response_model=RoleResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Cria um novo cargo"
)
async def criar_cargo(
    cargo: RoleCreate, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Cria um novo cargo com o nome e ID da classe de loja fornecidos."""
    return role_service.criar_cargo(db=db, cargo=cargo)

@router.get(
    "/", 
    response_model=List[RoleResponse], 
    summary="Lista todos os cargos"
)
async def listar_cargos(
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Retorna uma lista de todos os cargos cadastrados."""
    return role_service.obter_todos_cargos(db=db)

@router.get(
    "/{cargo_id}", 
    response_model=RoleResponse, 
    summary="Obtém um cargo pelo ID"
)
async def obter_cargo_por_id(
    cargo_id: int, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Retorna um cargo específico pelo seu ID."""
    cargo = role_service.obter_cargo_por_id(db=db, cargo_id=cargo_id)
    if not cargo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cargo não encontrado.")
    return cargo

@router.put(
    "/{cargo_id}", 
    response_model=RoleResponse, 
    summary="Atualiza um cargo"
)
async def atualizar_cargo(
    cargo_id: int, 
    cargo_atualizacao: RoleUpdate, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Atualiza as informações de um cargo existente."""
    return role_service.atualizar_cargo(db=db, cargo_id=cargo_id, cargo_atualizacao=cargo_atualizacao)

@router.delete(
    "/{cargo_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta um cargo"
)
async def deletar_cargo(
    cargo_id: int, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Deleta um cargo pelo ID."""
    role_service.deletar_cargo(db=db, cargo_id=cargo_id)
    return None
