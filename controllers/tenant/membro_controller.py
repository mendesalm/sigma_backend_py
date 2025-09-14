# backend_python/controllers/tenant/membro_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.membro_schema import MembroCreate, MembroUpdate, MembroResponse
from services import membro_service
from middleware.authorize_middleware import get_current_user # Usaremos a dependência principal de autorização

router = APIRouter()

@router.post(
    "/", 
    response_model=MembroResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Cria um novo membro para a loja"
)
def create_membro(
    membro: MembroCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Protege a rota
):
    """
    Cria um novo membro da loja. Apenas usuários autenticados (como Webmaster) podem realizar esta ação.
    - **membro**: Dados do membro a ser criado.
    """
    # A lógica de permissão mais granular pode ser adicionada aqui ou no service
    return membro_service.create_membro(db=db, membro_data=membro)

@router.get(
    "/", 
    response_model=List[MembroResponse],
    summary="Lista todos os membros da loja"
)
def get_all_membros(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Retorna uma lista de todos os membros da loja do tenant atual.
    """
    id_loja = current_user['tenant'].id
    return membro_service.get_all_membros_from_loja(db=db, loja_id=id_loja, skip=skip, limit=limit)

@router.get(
    "/{membro_id}", 
    response_model=MembroResponse, 
    summary="Busca um membro específico pelo ID"
)
def get_membro(
    membro_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna os detalhes de um membro específico.
    """
    # Adicionar validação para garantir que o membro pertence à loja do usuário logado
    return membro_service.get_membro_by_id(db=db, membro_id=membro_id)

@router.put(
    "/{membro_id}", 
    response_model=MembroResponse, 
    summary="Atualiza os dados de um membro"
)
def update_membro(
    membro_id: int, 
    membro: MembroUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza as informações de um membro existente.
    """
    # Adicionar validação para garantir que o membro pertence à loja do usuário logado
    return membro_service.update_membro(db=db, membro_id=membro_id, membro_data=membro)

@router.delete(
    "/{membro_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta um membro"
)
def delete_membro(
    membro_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Remove um membro do sistema.
    """
    # Adicionar validação para garantir que o membro pertence à loja do usuário logado
    membro_service.delete_membro(db=db, membro_id=membro_id)
    return
