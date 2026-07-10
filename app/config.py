import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://ventanilla:ventanilla@localhost:5432/ventanilla",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "cambia-esta-clave-en-produccion")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
    PDF_FOLDER = os.environ.get("PDF_FOLDER", os.path.join(BASE_DIR, "pdfs"))

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:4200")
