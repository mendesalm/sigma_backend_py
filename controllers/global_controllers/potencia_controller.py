# backend_python/controllers/global_controllers/potencia_controller.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
from schemas.potencia_schema import PotenciaCreate, PotenciaUpdate, PotenciaResponse
from services import potencia_service
from .super_admin_controller import get_current_super_admin

router = APIRouter()

@router.post("/", response_model=PotenciaResponse, status_code=status.HTTP_201_CREATED)
def create_potencia(potencia: PotenciaCreate, db: Session = Depends(get_db), admin: dict = Depends(get_current_super_admin)):
    return potencia_service.create_potencia(db=db, potencia=potencia)

# ... (GET, PUT, DELETE endpoints para Potencia)
