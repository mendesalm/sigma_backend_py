# backend_python/services/tenant_service.py

from sqlalchemy.orm import Session, joinedload
from models.models import Loja, Classe
from schemas.tenant_schema import TenantCreate, TenantUpdate
from fastapi import HTTPException, status

def create_tenant(db: Session, tenant: TenantCreate) -> Loja:
    # Verifica se a classe (potência) existe
    db_class = db.query(Classe).filter(Classe.id == tenant.id_classe).first()
    if not db_class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Classe com id {tenant.id_classe} não encontrada.")

    # Verifica se o código da loja já existe
    db_tenant = db.query(Loja).filter(Loja.codigo_loja == tenant.codigo_loja).first()
    if db_tenant:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Uma loja com este código já existe.")

    new_tenant = Loja(**tenant.model_dump())
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    return new_tenant

def get_tenant(db: Session, tenant_id: int) -> Loja:
    db_tenant = db.query(Loja).options(joinedload(Loja.classe)).filter(Loja.id == tenant_id).first()
    if not db_tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada.")
    return db_tenant

def get_all_tenants(db: Session):
    return db.query(Loja).options(joinedload(Loja.classe)).all()

def update_tenant(db: Session, tenant_id: int, tenant_update: TenantUpdate) -> Loja:
    db_tenant = get_tenant(db, tenant_id)

    update_data = tenant_update.model_dump(exclude_unset=True)
    
    # Se o id_classe for atualizado, verifica se a nova classe existe
    if "id_classe" in update_data:
        db_class = db.query(Classe).filter(Classe.id == update_data["id_classe"]).first()
        if not db_class:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Classe com id {update_data['id_classe']} não encontrada.")

    for key, value in update_data.items():
        setattr(db_tenant, key, value)
    
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

def delete_tenant(db: Session, tenant_id: int):
    db_tenant = get_tenant(db, tenant_id)
    
    # TODO: Adicionar verificação se a loja tem membros ou outras dependências antes de deletar
    
    db.delete(db_tenant)
    db.commit()
    return {"message": "Loja deletada com sucesso."}
