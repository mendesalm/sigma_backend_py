# backend_python/config/settings.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal, Union, List

class Configuracoes(BaseSettings):
    """
    Define e valida as variáveis de ambiente para a aplicação usando Pydantic.
    Carrega automaticamente as variáveis de um arquivo .env.
    """

    # --- Ambiente ---
    NODE_ENV: Literal["development", "staging", "production"] = Field(
        default="development",
        alias="NODE_ENV",
        description="Ambiente de execução da aplicação."
    )
    PORTA: int = Field(
        default=8000, 
        alias="PORT",
        description="Porta em que o servidor FastAPI será executado."
    )

    # --- Banco de Dados ---
    # O nome do banco de dados foi alterado para sigma_data, conforme solicitado.
    NOME_BANCO_DE_DADOS: str = Field(
        default="sigma_data", 
        alias="DB_GLOBAL_NAME",
        description="Nome do banco de dados principal."
    )
    USUARIO_BANCO_DE_DADOS: str = Field(alias="DB_GLOBAL_USER", description="Usuário do banco de dados.")
    SENHA_BANCO_DE_DADOS: str = Field(alias="DB_GLOBAL_PASS", min_length=8, description="Senha do banco de dados.")
    HOST_BANCO_DE_DADOS: str = Field(alias="DB_GLOBAL_HOST", description="Host do banco de dados.")
    PORTA_BANCO_DE_DADOS: int = Field(default=3306, alias="DB_GLOBAL_PORT", description="Porta do banco de dados.")
    DIALETO_BANCO_DE_DADOS: Literal["mysql", "postgresql"] = Field(
        default="mysql", 
        alias="DB_DIALECT",
        description="Dialeto do SQLAlchemy a ser usado (mysql ou postgresql)."
    )

    # --- JWT (JSON Web Token) ---
    SEGREDO_JWT: str = Field(
        alias="JWT_SECRET", 
        min_length=32, 
        description="Chave secreta para assinar os tokens JWT."
    )
    EXPIRACAO_JWT: str = Field(
        default="24h", 
        alias="JWT_EXPIRES_IN",
        description="Duração da validade de um token JWT (ex: '24h', '60m')."
    )

    # --- Logs ---
    NIVEL_LOG: Literal["error", "warn", "info", "debug"] = Field(
        default="info", 
        alias="LOG_LEVEL",
        description="Nível mínimo de log a ser registrado."
    )
    TAMANHO_MAX_LOG: Union[int, str] = Field(
        default="10m", 
        alias="LOG_MAX_SIZE",
        description="Tamanho máximo de cada arquivo de log."
    )
    MAX_ARQUIVOS_LOG: Union[int, str] = Field(
        default="14d", 
        alias="LOG_MAX_FILES",
        description="Número máximo de arquivos de log a serem mantidos."
    )

    # --- CORS (Cross-Origin Resource Sharing) ---
    ORIGEM_CORS: Union[str, List[str]] = Field(
        default="*", 
        alias="CORS_ORIGIN",
        description="Origens permitidas para requisições CORS."
    )

        # --- Configurações de Email ---
    EMAIL_HOST: str = Field(..., description="Host do servidor de e-mail SMTP.")
    EMAIL_PORT: int = Field(..., description="Porta do servidor de e-mail SMTP.")
    EMAIL_USER: str = Field(..., description="Usuário do e-mail para autenticação SMTP.")
    EMAIL_PASS: str = Field(..., description="Senha do e-mail para autenticação SMTP.")
    APP_NAME: str = Field("SiGMa", description="Nome da aplicação para o remetente de e-mail.")

    @property
    def URL_BANCO_DE_DADOS(self) -> str:
        """Monta a URL de conexão do banco de dados a partir das configurações."""
        # O dialeto para MySQL com PyMySQL é 'mysql+pymysql'
        dialeto_driver = f"{self.DIALETO_BANCO_DE_DADOS}+pymysql"
        return f"{dialeto_driver}://{self.USUARIO_BANCO_DE_DADOS}:{self.SENHA_BANCO_DE_DADOS}@{self.HOST_BANCO_DE_DADOS}:{self.PORTA_BANCO_DE_DADOS}/{self.NOME_BANCO_DE_DADOS}"

    # Configuração para carregar do arquivo .env
    _env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    model_config = SettingsConfigDict(env_file=_env_path, env_file_encoding='utf-8', extra='ignore')


# Instância única das configurações para ser usada em toda a aplicação
config = Configuracoes()

# Para teste rápido, você pode descomentar a linha abaixo
# print(config.model_dump_json(indent=2))

