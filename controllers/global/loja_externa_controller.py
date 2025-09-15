# backend_python/controllers/global/loja_externa_controller.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import connection
# from services import loja_externa_service
# from schemas import loja_externa_schema

router = APIRouter()

def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/lojas-externas/", response_model=loja_externa_schema.LojaExterna)
# def create_loja_externa(loja_externa: loja_externa_schema.LojaExternaCreate, db: Session = Depends(get_db)):
#     return loja_externa_service.create_loja_externa(db=db, loja_externa=loja_externa)

# @router.get("/lojas-externas/", response_model=list[loja_externa_schema.LojaExterna])
# def read_lojas_externas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     lojas_externas = loja_externa_service.get_lojas_externas(db, skip=skip, limit=limit)
#     return lojas_externas

# @router.get("/lojas-externas/{loja_externa_id}", response_model=loja_externa_schema.LojaExterna)
# def read_loja_externa(loja_externa_id: int, db: Session = Depends(get_db)):
#     db_loja_externa = loja_externa_service.get_loja_externa(db, loja_externa_id=loja_externa_id)
#     if db_loja_externa is None:
#         raise HTTPException(status_code=404, detail="LojaExterna not found")
#     return db_loja_externa