from models.productos import Productos
from utils.db import db

class ProductQueries:
    @staticmethod
    def obtener_productos():
        return Productos.query.filter_by(fk_estado=2).all()

    @staticmethod
    def buscar_prod_por_id(id_prod):
        return Productos.query.filter_by(id=id_prod).first()

    @staticmethod
    def agregar_producto(nombre, precio, categoria_id, estado):
        nuevo_producto = Productos(fk_categoria=categoria_id, nombre=nombre, precio=precio, fk_estado=estado)
        db.session.add(nuevo_producto)
        db.session.commit()

    @staticmethod
    def actualizar_producto(id, nombre, precio, categoria_id):
        producto = Productos.query.get(id)
        if producto:
            producto.nombre = nombre
            producto.precio = precio
            if categoria_id:
                producto.fk_categoria = categoria_id
            db.session.commit()

    @staticmethod
    def eliminar_producto(id):
        producto = Productos.query.get(id)
        if producto:
            producto.fk_estado = 1  
            db.session.commit()
