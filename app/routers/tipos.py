from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models import TipoSolicitud

tipos_bp = Blueprint("tipos", __name__, url_prefix="/api/v1/tipos-solicitud")


@tipos_bp.get("")
@jwt_required()
def listar_tipos():
    tipos = TipoSolicitud.query.order_by(TipoSolicitud.nombre).all()
    return jsonify([t.to_dict() for t in tipos])
