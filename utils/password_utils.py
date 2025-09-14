# backend_python/utils/password_utils.py

import secrets
import string

def generate_secure_password(length: int = 16) -> str:
    """Gera uma senha aleatória e segura."""
    # Caracteres permitidos na senha para garantir que seja URL-safe e fácil de manusear
    charset = string.ascii_letters + string.digits + "!@#$%^&*"
    
    # Gera uma senha usando o módulo secrets para segurança criptográfica
    password = ''.join(secrets.choice(charset) for i in range(length))
    
    return password
