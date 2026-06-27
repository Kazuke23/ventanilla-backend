import os
import uuid
from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.extensions import db
from app.models import Solicitud, TipoSolicitud
from app.core.security import requiere_rol
from app.services.email_service import enviar_notificacion_estado
from app.services.pdf_service import generar_pdf_comprobante

solicitudes_bp = Blueprint("solicitudes", __name__, url_prefix="/api/v1/solicitudes")

ESTADOS_VALIDOS = {"pendiente", "en_revision", "aprobada", "rechazada"}


@solicitudes_bp.get("")
@jwt_required()
def listar_solicitudes():
    claims = get_jwt()
    usuario_id = get_jwt_identity()
    estado = request.args.get("estado")

    query = Solicitud.query
    if claims.get("rol") == "estudiante":
        query = query.filter_by(usuario_id=usuario_id)
    if estado:
        query = query.filter_by(estado=estado)

    solicitudes = query.order_by(Solicitud.created_at.desc()).all()
    return jsonify([s.to_dict() for s in solicitudes])


@solicitudes_bp.post("")
@jwt_required()
@requiere_rol("estudiante")
def crear_solicitud():
    usuario_id = get_jwt_identity()
    tipo_id = request.form.get("tipo_id") or (request.json or {}).get("tipo_id") if request.is_json else request.form.get("tipo_id")
    motivo = request.form.get("motivo") or (request.json.get("motivo") if request.is_json else None)
    archivo = request.files.get("archivo")

    if not tipo_id:
        return jsonify({"error": "tipo_id es obligatorio"}), 400
    if not TipoSolicitud.query.get(tipo_id):
        return jsonify({"error": "tipo_id inválido"}), 400

    archivo_url = None
    if archivo:
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)
        nombre_seguro = f"{uuid.uuid4()}_{archivo.filename}"
        archivo.save(os.path.join(upload_folder, nombre_seguro))
        archivo_url = nombre_seguro

    solicitud = Solicitud(
        usuario_id=usuario_id,
        tipo_id=tipo_id,
        motivo=motivo,
        archivo_url=archivo_url,
        estado="pendiente",
    )
    db.session.add(solicitud)
    db.session.commit()

    return jsonify(solicitud.to_dict()), 201


@solicitudes_bp.get("/<solicitud_id>")
@jwt_required()
def detalle_solicitud(solicitud_id):
    claims = get_jwt()
    usuario_id = get_jwt_identity()

    solicitud = Solicitud.query.get_or_404(solicitud_id)
    if claims.get("rol") == "estudiante" and solicitud.usuario_id != usuario_id:
        return jsonify({"error": "No tienes acceso a esta solicitud"}), 403

    return jsonify(solicitud.to_dict())


@solicitudes_bp.put("/<solicitud_id>/estado")
@jwt_required()
@requiere_rol("funcionario")
def cambiar_estado(solicitud_id):
    data = request.get_json() or {}
    nuevo_estado = data.get("estado")
    respuesta = data.get("respuesta")

    if nuevo_estado not in ESTADOS_VALIDOS:
        return jsonify({"error": "Estado inválido"}), 400
    if nuevo_estado == "rechazada" and not respuesta:
        return jsonify({"error": "El campo respuesta es obligatorio al rechazar"}), 400

    solicitud = Solicitud.query.get_or_404(solicitud_id)
    solicitud.estado = nuevo_estado
    if respuesta:
        solicitud.respuesta = respuesta
    db.session.commit()

    if nuevo_estado == "aprobada":
        generar_pdf_comprobante(solicitud)

    if nuevo_estado in ("aprobada", "rechazada", "en_revision"):
        enviar_notificacion_estado(solicitud)

    return jsonify(solicitud.to_dict())


@solicitudes_bp.get("/<solicitud_id>/pdf")
@jwt_required()
def descargar_pdf(solicitud_id):
    claims = get_jwt()
    usuario_id = get_jwt_identity()

    solicitud = Solicitud.query.get_or_404(solicitud_id)
    if claims.get("rol") == "estudiante" and solicitud.usuario_id != usuario_id:
        return jsonify({"error": "No tienes acceso a esta solicitud"}), 403
    if solicitud.estado != "aprobada":
        return jsonify({"error": "El comprobante solo está disponible para solicitudes aprobadas"}), 400

    filepath = os.path.join(current_app.config["PDF_FOLDER"], f"comprobante_{solicitud.id}.pdf")
    if not os.path.exists(filepath):
        filepath = generar_pdf_comprobante(solicitud)

    return send_file(filepath, as_attachment=True, download_name=f"comprobante_{solicitud.id}.pdf")
