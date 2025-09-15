# backend_python/middleware/attendance_middleware.py

from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta
from services import sessao_maconica_service
from database import connection

async def check_attendance_window(request: Request):
    # This is a simplified example. A more robust solution should be implemented.
    # This middleware should be applied to the routes that register attendance.
    
    # get session id from path parameters
    sessao_id = request.path_params.get("sessao_id")
    if not sessao_id:
        return

    db = connection.SessionLocal()
    try:
        sessao = sessao_maconica_service.get_sessao(db, sessao_id)
        if not sessao:
            return

        now = datetime.now()
        start_time = sessao.data_sessao - timedelta(hours=2)
        end_time = sessao.data_sessao + timedelta(hours=2)

        if not (start_time <= now <= end_time):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Fora da janela de tempo para registro de presença."
            )
    finally:
        db.close()
