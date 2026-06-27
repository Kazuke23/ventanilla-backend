import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import current_app


def generar_pdf_comprobante(solicitud) -> str:
    """Genera el PDF de comprobante de una solicitud aprobada y devuelve la ruta del archivo."""
    folder = current_app.config["PDF_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    filename = f"comprobante_{solicitud.id}.pdf"
    filepath = os.path.join(folder, filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 80, "VENTANILLA — Comprobante de Solicitud")

    c.setFont("Helvetica", 11)
    lines = [
        f"N° de solicitud: {solicitud.id}",
        f"Estudiante: {solicitud.usuario.nombre}",
        f"Tipo de solicitud: {solicitud.tipo.nombre}",
        f"Estado: {solicitud.estado.upper()}",
        f"Fecha de creación: {solicitud.created_at.strftime('%Y-%m-%d %H:%M')}",
        f"Fecha de aprobación: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
    ]
    y = height - 130
    for line in lines:
        c.drawString(72, y, line)
        y -= 22

    c.setFont("Helvetica-Oblique", 9)
    c.drawString(72, 60, "Documento generado automáticamente por el sistema VENTANILLA.")
    c.save()

    return filepath
