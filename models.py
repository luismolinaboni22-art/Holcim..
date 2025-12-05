from datetime import datetime
from your_app import db

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    cedula = db.Column(db.String(20))
    empresa = db.Column(db.String(100))
    persona_a_visitar = db.Column(db.String(100))
    motivo = db.Column(db.String(200))
    placa = db.Column(db.String(20))
    hora_ingreso = db.Column(db.DateTime, default=datetime.utcnow)
    hora_salida = db.Column(db.DateTime, nullable=True)  # <-- aquí la salida
