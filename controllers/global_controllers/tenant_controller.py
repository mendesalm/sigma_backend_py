# backend_python/controllers/global_controllers/tenant_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.tenant_schema import TenantCreate, TenantUpdate, TenantResponse
from services import tenant_service
from controllers.global_controllers.super_admin_controller import get_current_super_admin

router = APIRouter()

@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED, summary="Cria uma nova Loja (Tenant)")
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_super_admin)):
    return tenant_service.create_tenant(db=db, tenant=tenant)

@router.get("/", response_model=List[TenantResponse], summary="Lista todas as Lojas (Tenants)")
def get_all_tenants(db: Session = Depends(get_db), current_admin: dict = Depends(get_current_super_admin)):
    return tenant_service.get_all_tenants(db=db)

@router.get("/{tenant_id}", response_model=TenantResponse, summary="Busca uma Loja por ID")
def get_tenant(tenant_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_super_admin)):
    return tenant_service.get_tenant(db=db, tenant_id=tenant_id)

@router.put("/{tenant_id}", response_model=TenantResponse, summary="Atualiza uma Loja")
def update_tenant(tenant_id: int, tenant_update: TenantUpdate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_super_admin)):
    return tenant_service.update_tenant(db=db, tenant_id=tenant_id, tenant_update=tenant_update)

@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deleta uma Loja")
def delete_tenant(tenant_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_super_admin)):
    tenant_service.delete_tenant(db=db, tenant_id=tenant_id)
    return
