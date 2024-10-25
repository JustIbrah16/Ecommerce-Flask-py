from models.productos import Productos
from models.categorias import Categorias
from utils.db import db

class ProductQueries:
    @staticmethod
    def obtener_productos():
        return Productos.query.all()

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

    @staticmethod
    def activar_producto(id):
        producto = Productos.query.get(id)
        if producto:
            categoria = Categorias.query.get(producto.fk_categioria)
            if categoria and categoria.fk_estado == 2:
                producto.fk_estado = 2  
                db.session.commit()
                return True
            else:
                return False
    
    @staticmethod
    def obtener_productos_disponibles():
        return Productos.query.filter(Productos.estado.has(id=2)).all()