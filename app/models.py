import uuid
from datetime import datetime
from app.extensions import db


def gen_uuid():
    return str(uuid.uuid4())


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    codigo = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # 'estudiante' | 'funcionario'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    solicitudes = db.relationship("Solicitud", backref="usuario", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "codigo": self.codigo,
            "rol": self.rol,
        }


class TipoSolicitud(db.Model):
    __tablename__ = "tipo_solicitud"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    dias_respuesta = db.Column(db.Integer, default=5)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "dias_respuesta": self.dias_respuesta,
        }


class Solicitud(db.Model):
    __tablename__ = "solicitud"

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    usuario_id = db.Column(db.String(36), db.ForeignKey("usuario.id"), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey("tipo_solicitud.id"), nullable=False)
    estado = db.Column(db.String(20), default="pendiente")  # pendiente|en_revision|aprobada|rechazada
    motivo = db.Column(db.Text)  # motivo aportado por el estudiante al crear
    respuesta = db.Column(db.Text)  # respuesta del funcionario (obligatoria si rechazada)
    archivo_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tipo = db.relationship("TipoSolicitud", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "usuario_nombre": self.usuario.nombre if self.usuario else None,
            "tipo_id": self.tipo_id,
            "tipo_nombre": self.tipo.nombre if self.tipo else None,
            "estado": self.estado,
            "motivo": self.motivo,
            "respuesta": self.respuesta,
            "archivo_url": self.archivo_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
