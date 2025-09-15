# backend_python/controllers/global/checkin_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import connection
from services import sessao_maconica_service, auth_service
from schemas import presenca_sessao_schema
from middleware.attendance_middleware import check_attendance_window
from models import models # Import models
from datetime import datetime

router = APIRouter()

def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/checkin", response_model=presenca_sessao_schema.PresencaSessao, dependencies=[Depends(check_attendance_window)])
async def checkin(
    loja_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.get_current_active_user) # Assuming this returns a dict with user info
):
    # This is a simplified implementation. More robust logic is needed.
    # It should check if the user is a member or a visitor.
    # It should also check if there is an active session for the lodge.

    # For now, let's assume the current_user is a member and we are creating a presence for them.
    # We need to find the active session for the given loja_id.
    # This part needs to be implemented based on how active sessions are determined.
    # For simplicity, let's assume we get the latest session for the lodge.
    sessao = db.query(models.SessaoMaconica).filter(models.SessaoMaconica.id_loja == loja_id).order_by(models.SessaoMaconica.data_sessao.desc()).first()

    if not sessao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active session found for this lodge.")

    # Assuming current_user contains id_membro
    id_membro = current_user.get("id") # Adjust based on actual user object structure

    # Check if attendance already exists for this member in this session
    existing_presenca = db.query(models.PresencaSessao).filter(
        models.PresencaSessao.id_sessao == sessao.id,
        models.PresencaSessao.id_membro == id_membro
    ).first()

    if existing_presenca:
        # Update existing attendance to 'Presente'
        existing_presenca.status_presenca = "Presente"
        existing_presenca.data_hora_checkin = datetime.now()
        db.commit()
        db.refresh(existing_presenca)
        return existing_presenca
    else:
        # Create new attendance record
        presenca_data = presenca_sessao_schema.PresencaSessaoCreate(
            id_sessao=sessao.id,
            id_membro=id_membro,
            status_presenca="Presente",
            data_hora_checkin=datetime.now()
        )
        db_presenca = models.PresencaSessao(**presenca_data.dict())
        db.add(db_presenca)
        db.commit()
        db.refresh(db_presenca)
        return db_presenca