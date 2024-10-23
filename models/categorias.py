from utils.db import db
from sqlalchemy import column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .estado import Estado 

class Categorias(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    fk_estado = db.Column(db.Integer, ForeignKey('estado.id'), nullable = False)
    nombre = db.Column(db.String, nullable = False)

    estado = relationship('Estado')

    def __init__(self, nombre):
        self.nombre = nombre
        