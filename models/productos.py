from utils.db import db
from sqlalchemy import column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, ForeignKey, relationship
from categorias import Categorias

class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    fk_categoria = db.column(db.Integer, ForeignKey('categorias.id'), nullable = False)
    nombre = db.Column(db.String, nullable = False)
    precio = db.column(db.Numeric(12, 2), nullable = False)
    categorias = relationship('Categorias')

    def __init__(self, id, fk_categoria, nombre, precio):
        self.id = id
        self.fk_categoria = fk_categoria
        self.nombre = nombre
        self.precio = precio