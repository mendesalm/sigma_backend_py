# backend_python/utils/email_sender.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

from config.settings import config

# Configura o logger para este módulo
logger = logging.getLogger(__name__)

async def send_email(to_email: str, subject: str, html_content: str):
    """Função para enviar um e-mail HTML usando as configurações do .env."""
    try:
        msg = MIMEMultipart("alternative")
        msg['From'] = f"{config.APP_NAME} <{config.EMAIL_USER}>"
        msg['To'] = to_email
        msg['Subject'] = subject

        # Anexa o conteúdo HTML
        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP_SSL(config.EMAIL_HOST, config.EMAIL_PORT) as server:
            server.login(config.EMAIL_USER, config.EMAIL_PASS)
            server.send_message(msg)
        
        logger.info(f"[EmailSender] E-mail enviado com sucesso para: {to_email}")
        return True
    except Exception as e:
        logger.error(f"[EmailSender] Falha ao enviar o e-mail para {to_email}: {e}")
        raise Exception("Não foi possível enviar o e-mail.")
