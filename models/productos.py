from utils.db import db
from sqlalchemy import column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .categorias import Categorias
from .estado import Estado

class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    fk_categoria = db.Column(db.Integer, ForeignKey('categorias.id'), nullable = False)
    fk_estado = db.Column(db.Integer, ForeignKey('estado.id'), nullable = False)
    nombre = db.Column(db.String, nullable = False)
    precio = db.Column(db.Numeric(12, 2), nullable = False)
    categorias = relationship('Categorias')
    estado = relationship('Estado')

    def __init__(self, fk_categoria, fk_estado, nombre, precio):
        self.fk_categoria = fk_categoria
        self.fk_estado = fk_estado
        self.nombre = nombre
        self.precio = precio

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio
        }    