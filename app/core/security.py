from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt


def requiere_rol(*roles_permitidos):
    """Decorador que exige que el usuario autenticado tenga uno de los roles indicados.
    Debe usarse siempre DESPUÉS de @jwt_required()."""

    def decorador(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("rol") not in roles_permitidos:
                return jsonify({"error": "No tienes permisos para realizar esta acción"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorador
