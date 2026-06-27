"""Script para inicializar la base de datos con tipos de solicitud y usuarios de prueba.
Ejecutar con: python seed.py
"""
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import Usuario, TipoSolicitud

app = create_app()

with app.app_context():
    db.create_all()

    if not TipoSolicitud.query.first():
        tipos = [
            TipoSolicitud(nombre="Certificado de matrícula", descripcion="Certifica matrícula vigente", dias_respuesta=3),
            TipoSolicitud(nombre="Constancia de notas", descripcion="Reporte de calificaciones del periodo", dias_respuesta=5),
            TipoSolicitud(nombre="Paz y salvo", descripcion="Constancia de no tener obligaciones pendientes", dias_respuesta=5),
            TipoSolicitud(nombre="Carta de presentación", descripcion="Carta para prácticas o pasantías", dias_respuesta=2),
        ]
        db.session.add_all(tipos)

    if not Usuario.query.filter_by(email="estudiante@uni.edu").first():
        db.session.add(Usuario(
            nombre="Ana Estudiante",
            email="estudiante@uni.edu",
            codigo="EST001",
            password_hash=generate_password_hash("estudiante123"),
            rol="estudiante",
        ))

    if not Usuario.query.filter_by(email="funcionario@uni.edu").first():
        db.session.add(Usuario(
            nombre="Carlos Funcionario",
            email="funcionario@uni.edu",
            codigo="FUN001",
            password_hash=generate_password_hash("funcionario123"),
            rol="funcionario",
        ))

    db.session.commit()
    print("Base de datos inicializada con datos de prueba.")
