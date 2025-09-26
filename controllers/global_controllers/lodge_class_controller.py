# backend_python/controllers/global_controllers/lodge_class_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.lodge_class_schema import LodgeClassCreate, LodgeClassUpdate, LodgeClassResponse
from services import lodge_class_service
from controllers.global_controllers.super_admin_controller import get_current_super_admin

router = APIRouter()

@router.post("/", response_model=LodgeClassResponse, status_code=status.HTTP_201_CREATED, summary="Cria uma nova Classe (Potência)")
def create_lodge_class(lodge_class: LodgeClassCreate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_super_admin)):
    """Cria uma nova Classe (Potência) no sistema."""
    return lodge_class_service.create_lodge_class(db=db, lodge_class=lodge_class)

@router.get("/", response_model=List[LodgeClassResponse], summary="Lista todas as Classes (Potências)")
def get_all_lodge_classes(db: Session = Depends(get_db), current_admin: dict = Depends(get_current_super_admin)):
    """Retorna uma lista de todas as Classes (Potências)."""
    return lodge_class_service.get_all_lodge_classes(db=db)

@router.get("/{lodge_class_id}", response_model=LodgeClassResponse, summary="Busca uma Classe por ID")
def get_lodge_class(lodge_class_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_super_admin)):
    """Busca uma Classe (Potência) específica pelo seu ID."""
    return lodge_class_service.get_lodge_class(db=db, lodge_class_id=lodge_class_id)

@router.put("/{lodge_class_id}", response_model=LodgeClassResponse, summary="Atualiza uma Classe")
def update_lodge_class(lodge_class_id: int, lodge_class_update: LodgeClassUpdate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_super_admin)):
    """Atualiza as informações de uma Classe (Potência) existente."""
    return lodge_class_service.update_lodge_class(db=db, lodge_class_id=lodge_class_id, lodge_class_update=lodge_class_update)

@router.delete("/{lodge_class_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deleta uma Classe")
def delete_lodge_class(lodge_class_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_super_admin)):
    """Deleta uma Classe (Potência) pelo seu ID."""
    lodge_class_service.delete_lodge_class(db=db, lodge_class_id=lodge_class_id)
    return