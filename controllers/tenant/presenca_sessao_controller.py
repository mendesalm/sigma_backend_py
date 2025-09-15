# backend_python/controllers/tenant/presenca_sessao_controller.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import connection
from services import presenca_sessao_service
from schemas import presenca_sessao_schema

router = APIRouter()

def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/presencas/", response_model=presenca_sessao_schema.PresencaSessao)
def create_presenca_sessao(presenca_sessao: presenca_sessao_schema.PresencaSessaoCreate, db: Session = Depends(get_db)):
    return presenca_sessao_service.create_presenca_sessao(db=db, presenca_sessao=presenca_sessao)

@router.get("/presencas/", response_model=list[presenca_sessao_schema.PresencaSessao])
def read_presencas_sessao(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    presencas_sessao = presenca_sessao_service.get_presencas_sessao(db, skip=skip, limit=limit)
    return presencas_sessao

@router.get("/presencas/{presenca_sessao_id}", response_model=presenca_sessao_schema.PresencaSessao)
def read_presenca_sessao(presenca_sessao_id: int, db: Session = Depends(get_db)):
    db_presenca_sessao = presenca_sessao_service.get_presenca_sessao(db, presenca_sessao_id=presenca_sessao_id)
    if db_presenca_sessao is None:
        raise HTTPException(status_code=404, detail="PresencaSessao not found")
    return db_presenca_sessao
