# backend_python/utils/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

from config.settings import config

# Garante que o diretório de logs exista
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configuração básica do logger
logger = logging.getLogger(__name__)
logger.setLevel(config.NIVEL_LOG.upper()) # Define o nível de log a partir das configurações

# Formato do log
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Handler para arquivo de erros
error_file_handler = RotatingFileHandler(
    os.path.join(log_dir, 'error.log'),
    maxBytes=config.TAMANHO_MAX_LOG if isinstance(config.TAMANHO_MAX_LOG, int) else int(config.TAMANHO_MAX_LOG[:-1]) * 1024 * 1024, # Converte '10m' para bytes
    backupCount=int(config.MAX_ARQUIVOS_LOG[:-1]) if isinstance(config.MAX_ARQUIVOS_LOG, str) and config.MAX_ARQUIVOS_LOG.endswith('d') else 14 # Converte '14d' para número de arquivos
)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)
logger.addHandler(error_file_handler)

# Handler para arquivo combinado
combined_file_handler = RotatingFileHandler(
    os.path.join(log_dir, 'combined.log'),
    maxBytes=config.TAMANHO_MAX_LOG if isinstance(config.TAMANHO_MAX_LOG, int) else int(config.TAMANHO_MAX_LOG[:-1]) * 1024 * 1024,
    backupCount=int(config.MAX_ARQUIVOS_LOG[:-1]) if isinstance(config.MAX_ARQUIVOS_LOG, str) and config.MAX_ARQUIVOS_LOG.endswith('d') else 14
)
combined_file_handler.setLevel(logging.INFO) # Ou o nível configurado
combined_file_handler.setFormatter(formatter)
logger.addHandler(combined_file_handler)

# Handler para console (apenas em desenvolvimento)
if config.NODE_ENV != 'production':
    console_handler = logging.StreamHandler()
    console_handler.setLevel(config.NIVEL_LOG.upper())
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Exemplo de uso:
# logger.info("Esta é uma mensagem de informação.")
# logger.error("Este é um erro!")
