# backend_python/utils/api_key_utils.py

import secrets

def generate_api_key() -> str:
    """Gera uma API Key segura e aleatória (64 caracteres hex)."""
    return secrets.token_hex(32)
