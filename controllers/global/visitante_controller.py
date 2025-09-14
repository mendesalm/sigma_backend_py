# backend_python/controllers/global/visitante_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.visitante_schema import VisitanteCreate, VisitanteUpdate, VisitanteResponse
from services import visitante_service
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
    response_model=VisitanteResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Cria um novo visitante"
)
def create_visitante(
    visitante: VisitanteCreate, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """
    Cria um novo registro de visitante. Apenas Super Administradores podem realizar esta ação.
    """
    return visitante_service.create_visitante(db=db, visitante_data=visitante)

@router.get(
    "/", 
    response_model=List[VisitanteResponse],
    summary="Lista todos os visitantes"
)
def get_all_visitantes(
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin),
    skip: int = 0,
    limit: int = 100
):
    """
    Retorna uma lista de todos os visitantes cadastrados.
    """
    return visitante_service.get_all_visitantes(db=db, skip=skip, limit=limit)

@router.get(
    "/{visitante_id}", 
    response_model=VisitanteResponse, 
    summary="Busca um visitante específico pelo ID"
)
def get_visitante(
    visitante_id: int, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """
    Retorna os detalhes de um visitante específico.
    """
    return visitante_service.get_visitante_by_id(db=db, visitante_id=visitante_id)

@router.put(
    "/{visitante_id}", 
    response_model=VisitanteResponse, 
    summary="Atualiza os dados de um visitante"
)
def update_visitante(
    visitante_id: int, 
    visitante: VisitanteUpdate, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """
    Atualiza as informações de um visitante existente.
    """
    return visitante_service.update_visitante(db=db, visitante_id=visitante_id, visitante_data=visitante)

@router.delete(
    "/{visitante_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta um visitante"
)
def delete_visitante(
    visitante_id: int, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """
    Remove um visitante do sistema.
    """
    visitante_service.delete_visitante(db=db, visitante_id=visitante_id)
    return
