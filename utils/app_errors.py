# backend_python/utils/app_errors.py

from fastapi import HTTPException, status

class AppError(HTTPException):
    """Exceção personalizada para erros de aplicação com status HTTP."""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)
