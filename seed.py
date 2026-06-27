"""Script para inicializar la base de datos con tipos de solicitud y usuarios de prueba.
Ejecutar con: python seed.py
"""
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import Usuario, TipoSolicitud, Area

app = create_app()

with app.app_context():
    db.create_all()

    # ==========================
    # Crear áreas
    # ==========================
    if not Area.query.first():
        cartera = Area(
            nombre="Cartera",
            correo="cartera@unicatolica.edu.co"
        )

        registro = Area(
            nombre="Registro Académico",
            correo="registro@unicatolica.edu.co"
        )

        bienestar = Area(
            nombre="Bienestar Universitario",
            correo="bienestar@unicatolica.edu.co"
        )

        practicas = Area(
            nombre="Prácticas y Pasantías",
            correo="practicas@unicatolica.edu.co"
        )

        db.session.add_all([
            cartera,
            registro,
            bienestar,
            practicas
        ])

        db.session.commit()

    cartera = Area.query.filter_by(nombre="Cartera").first()
    registro = Area.query.filter_by(nombre="Registro Académico").first()
    practicas = Area.query.filter_by(nombre="Prácticas y Pasantías").first()

    # ==========================
    # Tipos de solicitud
    # ==========================
    if not TipoSolicitud.query.first():

        tipos = [

            TipoSolicitud(
                nombre="Certificado de matrícula",
                descripcion="Certifica matrícula vigente",
                dias_respuesta=3,
                area_id=registro.id
            ),

            TipoSolicitud(
                nombre="Constancia de notas",
                descripcion="Reporte de calificaciones",
                dias_respuesta=5,
                area_id=registro.id
            ),

            TipoSolicitud(
                nombre="Paz y salvo",
                descripcion="Constancia de obligaciones",
                dias_respuesta=5,
                area_id=cartera.id
            ),

            TipoSolicitud(
                nombre="Factura semestre",
                descripcion="Generación de factura",
                dias_respuesta=2,
                area_id=cartera.id
            ),

            TipoSolicitud(
                nombre="Carta de presentación",
                descripcion="Prácticas empresariales",
                dias_respuesta=2,
                area_id=practicas.id
            ),
        ]

        db.session.add_all(tipos)

    # ==========================
    # Estudiante
    # ==========================
    if not Usuario.query.filter_by(email="estudiante@uni.edu").first():

        db.session.add(
            Usuario(
                nombre="Ana Estudiante",
                email="estudiante@uni.edu",
                codigo="EST001",
                password_hash=generate_password_hash("estudiante123"),
                rol="estudiante"
            )
        )

    # ==========================
    # Funcionario Registro
    # ==========================
    if not Usuario.query.filter_by(email="funcionario@uni.edu").first():

        db.session.add(
            Usuario(
                nombre="Carlos Funcionario",
                email="funcionario@uni.edu",
                codigo="FUN001",
                password_hash=generate_password_hash("funcionario123"),
                rol="funcionario",
                area_id=registro.id
            )
        )

    db.session.commit()

    print("Base de datos inicializada correctamente.")