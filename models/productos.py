from utils.db import db
from sqlalchemy import column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .categorias import Categorias

class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    fk_categoria = db.Column(db.Integer, ForeignKey('categorias.id'), nullable = False)
    nombre = db.Column(db.String, nullable = False)
    precio = db.Column(db.Numeric(12, 2), nullable = False)
    categorias = relationship('Categorias')

    def __init__(self, fk_categoria, nombre, precio):
        self.fk_categoria = fk_categoria
        self.nombre = nombre
        self.precio = precio