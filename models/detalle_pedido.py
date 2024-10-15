from utils.db import db
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .pedidos import Pedidos
from .productos import Productos
from .categorias import Categorias

class Detalle_pedido(db.Model):
    __tablename__ = 'detalle_pedido'
    
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    fk_pedido = db.Column(db.Integer, ForeignKey('pedidos.id'), nullable = False)
    fk_producto = db.Column(db.Integer, ForeignKey('productos.id'), nullable = False)
    fk_categoria = db.Column(db.Integer, ForeignKey('categorias.id'), nullable = False)
    cantidad = db.Column(db.Integer, nullable = False)
    subtotal = db.Column(db.Numeric(12, 2), nullable = False)

    pedido = relationship('Pedidos')
    producto = relationship('Productos')
    categoria =  relationship('Categorias')

    def __init__(self, fk_pedido, fk_producto, fk_categoria, cantidad, subtotal):
        self.fk_pedido = fk_pedido
        self.fk_producto = fk_producto
        self.fk_categoria = fk_categoria
        self.cantidad = cantidad
        self.subtotal = subtotal