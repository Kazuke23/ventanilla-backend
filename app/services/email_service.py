from flask import current_app
from flask_mail import Mail, Message

mail = Mail()

PLANTILLAS = {
    "en_revision": "Tu solicitud {tipo} (#{id}) está ahora en revisión.",
    "aprobada": "Tu solicitud {tipo} (#{id}) fue APROBADA. Ya puedes descargar tu comprobante en la plataforma.",
    "rechazada": "Tu solicitud {tipo} (#{id}) fue RECHAZADA.\nMotivo: {respuesta}",
}


def enviar_notificacion_estado(solicitud):
    """Envía un correo al estudiante notificando el cambio de estado de su solicitud."""
    cuerpo = PLANTILLAS.get(solicitud.estado, "El estado de tu solicitud cambió a {estado}.").format(
        tipo=solicitud.tipo.nombre,
        id=solicitud.id,
        estado=solicitud.estado,
        respuesta=solicitud.respuesta or "",
    )
    try:
        msg = Message(
            subject=f"VENTANILLA — Actualización de tu solicitud #{solicitud.id}",
            recipients=[solicitud.usuario.email],
            body=cuerpo,
        )
        mail.send(msg)
    except Exception as e:
        # En el MVP no bloqueamos la operación si falla el envío de correo
        current_app.logger.warning(f"No se pudo enviar el email de notificación: {e}")
