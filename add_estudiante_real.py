"""Script para agregar un estudiante de prueba con correo real.
Ejecutar con: python add_estudiante_real.py
"""
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import Usuario

app = create_app()

with app.app_context():
    email = "sebastian.buitrago01@unicatolica.edu.co"

    if not Usuario.query.filter_by(email=email).first():
        db.session.add(
            Usuario(
                nombre="Sebastian Buitrago",
                email=email,
                codigo="398791",
                password_hash=generate_password_hash("estudiante123"),
                rol="estudiante"
            )
        )
        db.session.commit()
        print(f"Usuario {email} creado correctamente.")
    else:
        print(f"El usuario {email} ya existe, no se creó de nuevo.")