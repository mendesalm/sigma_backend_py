# backend_python/services/lodge_class_service.py

from sqlalchemy.orm import Session
from models.models import Classe
from schemas.lodge_class_schema import LodgeClassCreate, LodgeClassUpdate
from fastapi import HTTPException, status

def create_lodge_class(db: Session, lodge_class: LodgeClassCreate) -> Classe:
    """Cria uma nova Classe (Potência)."""
    db_lodge_class = db.query(Classe).filter(Classe.nome == lodge_class.nome).first()
    if db_lodge_class:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Uma classe com este nome já existe.")
    
    new_lodge_class = Classe(**lodge_class.model_dump())
    db.add(new_lodge_class)
    db.commit()
    db.refresh(new_lodge_class)
    return new_lodge_class

def get_lodge_class(db: Session, lodge_class_id: int) -> Classe:
    """Busca uma única classe pelo ID."""
    db_lodge_class = db.query(Classe).filter(Classe.id == lodge_class_id).first()
    if not db_lodge_class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classe não encontrada.")
    return db_lodge_class

def get_all_lodge_classes(db: Session):
    """Retorna todas as classes."""
    return db.query(Classe).all()

def update_lodge_class(db: Session, lodge_class_id: int, lodge_class_update: LodgeClassUpdate) -> Classe:
    """Atualiza uma classe existente."""
    db_lodge_class = get_lodge_class(db, lodge_class_id)

    update_data = lodge_class_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_lodge_class, key, value)
    
    db.add(db_lodge_class)
    db.commit()
    db.refresh(db_lodge_class)
    return db_lodge_class

def delete_lodge_class(db: Session, lodge_class_id: int):
    """Deleta uma classe."""
    db_lodge_class = get_lodge_class(db, lodge_class_id)
    
    # Adicionar aqui lógica para verificar se a classe está em uso antes de deletar, se necessário

    db.delete(db_lodge_class)
    db.commit()
    return {"message": "Classe deletada com sucesso."}