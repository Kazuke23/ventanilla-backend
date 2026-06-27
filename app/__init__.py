from flask import Flask
from app.config import Config
from app.extensions import db, jwt, cors
from app.services.email_service import mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    from app.routers.auth import auth_bp
    from app.routers.tipos import tipos_bp
    from app.routers.solicitudes import solicitudes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tipos_bp)
    app.register_blueprint(solicitudes_bp)

    @app.get("/api/v1/health")
    def health():
        return {"status": "ok", "service": "ventanilla-api"}

    return app
