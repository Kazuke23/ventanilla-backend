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
    area_id = db.Column(
    db.Integer,
    db.ForeignKey("area.id"),
    nullable=True
)
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


class Area(db.Model):
    __tablename__ = "area"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    correo = db.Column(db.String(150), nullable=True)

    tipos = db.relationship("TipoSolicitud", backref="area", lazy=True)
    funcionarios = db.relationship("Usuario", backref="area", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
        }


class TipoSolicitud(db.Model):
    __tablename__ = "tipo_solicitud"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    dias_respuesta = db.Column(db.Integer, default=5)
    
    area_id = db.Column(
    db.Integer,
    db.ForeignKey("area.id"),
    nullable=False
)
    

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "dias_respuesta": self.dias_respuesta,
            "area_id": self.area_id,
            "area_nombre": self.area.nombre if self.area else None,
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
