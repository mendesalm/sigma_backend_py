# backend_python/controllers/global/lodge_class_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.lodge_class_schema import LodgeClassCreate, LodgeClassUpdate, LodgeClassResponse
from services import lodge_class_service
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
    response_model=LodgeClassResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Cria uma nova classe de loja"
)
async def criar_classe_loja(
    classe_loja: LodgeClassCreate, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Cria uma nova classe de loja com o nome e descrição fornecidos."""
    return lodge_class_service.criar_classe_loja(db=db, classe_loja=classe_loja)

@router.get(
    "/", 
    response_model=List[LodgeClassResponse], 
    summary="Lista todas as classes de loja"
)
async def listar_classes_loja(
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Retorna uma lista de todas as classes de loja cadastradas."""
    return lodge_class_service.obter_todas_classes_loja(db=db)

@router.get(
    "/{classe_loja_id}", 
    response_model=LodgeClassResponse, 
    summary="Obtém uma classe de loja pelo ID"
)
async def obter_classe_loja_por_id(
    classe_loja_id: int, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Retorna uma classe de loja específica pelo seu ID."""
    classe_loja = lodge_class_service.obter_classe_loja_por_id(db=db, classe_loja_id=classe_loja_id)
    if not classe_loja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classe de Loja não encontrada.")
    return classe_loja

@router.put(
    "/{classe_loja_id}", 
    response_model=LodgeClassResponse, 
    summary="Atualiza uma classe de loja"
)
async def atualizar_classe_loja(
    classe_loja_id: int, 
    classe_loja_atualizacao: LodgeClassUpdate, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Atualiza as informações de uma classe de loja existente."""
    return lodge_class_service.atualizar_classe_loja(db=db, classe_loja_id=classe_loja_id, classe_loja_atualizacao=classe_loja_atualizacao)

@router.delete(
    "/{classe_loja_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta uma classe de loja"
)
async def deletar_classe_loja(
    classe_loja_id: int, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Deleta uma classe de loja pelo ID."""
    lodge_class_service.deletar_classe_loja(db=db, classe_loja_id=classe_loja_id)
    return None
