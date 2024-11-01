from utils.db import db

class Permisos(db.Model):
    __tablename__ = 'permisos'
    id = db.Column(db.Integer, primary_key=True)  # Asegúrate de que sea Integer
    nombre = db.Column(db.String, nullable=False)
