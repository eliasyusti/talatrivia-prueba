import logging
from app.admin.models.preguntas_model import Difficulty
from sqlalchemy.orm import Session
from app.settings.database import get_db, Base, engine
from app.usuarios.models.user import User, Role
from app.auth.auth import hash_password


def create_tables():
    """Crea las tablas en la base de datos si no existen."""
    Base.metadata.create_all(bind=engine)
    logging.info("✅ Tablas creadas correctamente")


def seed_roles_and_admin():
    """Crea los roles 'Admin' y 'User' por defecto y un usuario administrador."""
    db: Session = next(get_db())

    # Verificar si los roles ya existen
    admin_role = db.query(Role).filter_by(name="Admin").first()
    user_role = db.query(Role).filter_by(name="User").first()

    if not admin_role:
        admin_role = Role(name="Admin")
        db.add(admin_role)

    if not user_role:
        user_role = Role(name="User")
        db.add(user_role)

    db.commit()

    # Verificar si el usuario admin ya existe
    admin_email = "admin@example.com"
    admin_user = db.query(User).filter_by(email=admin_email).first()

    if not admin_user:
        hashed_pwd = hash_password("admin123")  # Contraseña predeterminada
        admin_user = User(
            name="Admin User",
            email=admin_email,
            hashed_password=hashed_pwd,
            role_id=admin_role.id,  # Asignar el rol de Admin
        )
        db.add(admin_user)
        db.commit()

    logging.info("✅ Roles y usuario administrador creados correctamente")


def seed_difficulties():
    """Crea las dificultades por defecto si no existen."""
    db: Session = next(get_db())

    default_difficulties = ["Fácil", "Medio", "Difícil"]
    existing_difficulties = db.query(Difficulty).count()

    if existing_difficulties == 0:
        for difficulty in default_difficulties:
            db.add(Difficulty(name=difficulty))
        db.commit()

    logging.info("✅ Dificultades creadas correctamente")
