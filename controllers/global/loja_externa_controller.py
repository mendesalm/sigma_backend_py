# backend_python/controllers/global/loja_externa_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.loja_externa_schema import LojaExternaCreate, LojaExternaUpdate, LojaExternaResponse
from services import loja_externa_service
from middleware.authorize_middleware import get_current_user # Usaremos a dependência principal de autorização
from models.models import SuperAdministrador # Para validação de perfil

router = APIRouter()

# Dependência para garantir que o usuário é um SuperAdmin
async def get_current_super_admin(current_user_data: dict = Depends(get_current_user)) -> SuperAdministrador:
    """
    Verifica se o usuário atual é um SuperAdmin e retorna o objeto do usuário.
    Levanta uma exceção HTTPException se o perfil não for 'super_admin'.
    """
    if current_user_data.get("perfil") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas Super Administradores podem realizar esta ação."
        )
    return current_user_data.get("user")

@router.post(
    "/", 
    response_model=LojaExternaResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Cria uma nova loja externa"
)
def create_loja_externa(
    loja_externa: LojaExternaCreate, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """
    Cria um novo registro de loja externa. Apenas Super Administradores podem realizar esta ação.
    """
    return loja_externa_service.create_loja_externa(db=db, loja_externa_data=loja_externa)

@router.get(
    "/", 
    response_model=List[LojaExternaResponse],
    summary="Lista todas as lojas externas"
)
def get_all_lojas_externas(
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin),
    skip: int = 0,
    limit: int = 100
):
    """
    Retorna uma lista de todas as lojas externas cadastradas.
    """
    return loja_externa_service.get_all_lojas_externas(db=db, skip=skip, limit=limit)

@router.get(
    "/{loja_externa_id}", 
    response_model=LojaExternaResponse, 
    summary="Busca uma loja externa específica pelo ID"
)
def get_loja_externa(
    loja_externa_id: int, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """
    Retorna os detalhes de uma loja externa específica.
    """
    return loja_externa_service.get_loja_externa_by_id(db=db, loja_externa_id=loja_externa_id)

@router.put(
    "/{loja_externa_id}", 
    response_model=LojaExternaResponse, 
    summary="Atualiza os dados de uma loja externa"
)
def update_loja_externa(
    loja_externa_id: int, 
    loja_externa: LojaExternaUpdate, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """
    Atualiza as informações de uma loja externa existente.
    """
    return loja_externa_service.update_loja_externa(db=db, loja_externa_id=loja_externa_id, loja_externa_data=loja_externa)

@router.delete(
    "/{loja_externa_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta uma loja externa"
)
def delete_loja_externa(
    loja_externa_id: int, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """
    Remove uma loja externa do sistema.
    """
    loja_externa_service.delete_loja_externa(db=db, loja_externa_id=loja_externa_id)
    return
