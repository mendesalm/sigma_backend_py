# backend_python/controllers/tenant/sessao_maconica_controller.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import connection
from services import sessao_maconica_service
from schemas import sessao_maconica_schema, presenca_sessao_schema, visitante_schema

router = APIRouter()

def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sessoes/", response_model=sessao_maconica_schema.SessaoMaconica)
def create_sessao(sessao: sessao_maconica_schema.SessaoMaconicaCreate, loja_id: int, db: Session = Depends(get_db)):
    return sessao_maconica_service.create_sessao(db=db, sessao=sessao, loja_id=loja_id)

@router.get("/sessoes/", response_model=list[sessao_maconica_schema.SessaoMaconica])
def read_sessoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sessoes = sessao_maconica_service.get_sessoes(db, skip=skip, limit=limit)
    return sessoes

@router.get("/sessoes/{sessao_id}", response_model=sessao_maconica_schema.SessaoMaconica)
def read_sessao(sessao_id: int, db: Session = Depends(get_db)):
    db_sessao = sessao_maconica_service.get_sessao(db, sessao_id=sessao_id)
    if db_sessao is None:
        raise HTTPException(status_code=404, detail="Sessao not found")
    return db_sessao

@router.put("/sessoes/{sessao_id}/attendance", response_model=sessao_maconica_schema.SessaoMaconica)
def update_sessa_attendance(sessao_id: int, attendance_data: list[presenca_sessao_schema.PresencaSessaoBase], db: Session = Depends(get_db)):
    return sessao_maconica_service.update_session_attendance(db=db, sessao_id=sessao_id, attendance_data=attendance_data)

@router.post("/sessoes/{sessao_id}/visitors", response_model=visitante_schema.Visitante)
def manage_session_visitor(sessao_id: int, visitor_data: visitante_schema.VisitanteCreate, db: Session = Depends(get_db)):
    return sessao_maconica_service.manage_session_visitor(db=db, sessao_id=sessao_id, visitor_data=visitor_data)

@router.delete("/sessoes/visitors/{visitor_id}")
def remove_session_visitor(visitor_id: int, db: Session = Depends(get_db)):
    return sessao_maconica_service.remove_session_visitor(db=db, visitor_id=visitor_id)
