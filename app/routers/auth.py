from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app.extensions import db
from app.models import Usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email y password son obligatorios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not check_password_hash(usuario.password_hash, password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = create_access_token(
        identity=usuario.id,
        additional_claims={"rol": usuario.rol, "nombre": usuario.nombre},
    )
    return jsonify({"access_token": token, "usuario": usuario.to_dict()})


@auth_bp.get("/me")
@jwt_required()
def me():
    usuario_id = get_jwt_identity()
    usuario = db.session.get(Usuario, usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario.to_dict())
