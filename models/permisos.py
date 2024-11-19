from utils.db import db
from sqlalchemy.orm import relationship
from models.grupos import Grupos
from sqlalchemy import Integer, String, ForeignKey  # Importa ForeignKey

class Permisos(db.Model):
    __tablename__ = 'permisos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    fk_grupo = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=True)  # Aquí se define la clave foránea

    grupo = relationship('Grupos')  # Esto define la relación
