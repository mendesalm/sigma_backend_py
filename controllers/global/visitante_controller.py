# backend_python/controllers/global/visitante_controller.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import connection
# from services import visitante_service
# from schemas import visitante_schema

router = APIRouter()

def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/visitantes/", response_model=visitante_schema.Visitante)
# def create_visitante(visitante: visitante_schema.VisitanteCreate, db: Session = Depends(get_db)):
#     return visitante_service.create_visitante(db=db, visitante=visitante)

# @router.get("/visitantes/", response_model=list[visitante_schema.Visitante])
# def read_visitantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     visitantes = visitante_service.get_visitantes(db, skip=skip, limit=limit)
#     return visitantes

# @router.get("/visitantes/{visitante_id}", response_model=visitante_schema.Visitante)
# def read_visitante(visitante_id: int, db: Session = Depends(get_db)):
#     db_visitante = visitante_service.get_visitante(db, visitante_id=visitante_id)
#     if db_visitante is None:
#         raise HTTPException(status_code=404, detail="Visitante not found")
#     return db_visitante