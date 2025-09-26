import bcrypt
from sqlalchemy import select
from database.connection import SessionLocal
from models.models import SuperAdministrador
from config.settings import config

def seed_database():
    """
    Popula o banco de dados com o usuário Super Administrador de forma síncrona.
    """
    db = SessionLocal()
    try:
        super_admin_email = config.ROOT_EMAIL
        
        existing_super_admin = db.execute(
            select(SuperAdministrador).where(SuperAdministrador.email == super_admin_email)
        ).scalars().first()

        if not existing_super_admin:
            print(f"Criando super admin com o e-mail '{super_admin_email}'...")
            
            # CORREÇÃO FINAL: Usa a biblioteca bcrypt diretamente para o hash
            password_bytes = config.ROOT_PASSWORD.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
            
            new_super_admin = SuperAdministrador(
                nome_usuario="superadmin",
                email=super_admin_email,
                senha_hash=hashed_password,
                esta_ativo=True
            )
            db.add(new_super_admin)
            db.commit()
            print(f"Super admin '{super_admin_email}' criado com sucesso.")
        else:
            print(f"Super admin com o e-mail '{super_admin_email}' já existe. Nenhuma ação foi tomada.")

    finally:
        db.close()

if __name__ == "__main__":
    print("Iniciando o processo de seeding do banco de dados...")
    seed_database()
    print("Seeding do banco de dados concluído.")
