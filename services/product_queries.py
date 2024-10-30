from models.productos import Productos
from models.categorias import Categorias
from utils.db import db
from utils.historial import Historial

ESTADO_INACTIVO = 1
ESTADO_ACTIVO = 2
class ProductQueries:
    @staticmethod
    def obtener_productos():
        return Productos.query.all()

    @staticmethod
    def buscar_prod_por_id(id_prod):
        return Productos.query.filter_by(id=id_prod).first()

    @staticmethod
    def agregar_producto(nombre, precio, categoria_id, estado):
        try:
            Historial.historial_categorias()
            nuevo_producto = Productos(fk_categoria=categoria_id, nombre=nombre, precio=precio, fk_estado=estado)
            db.session.add(nuevo_producto)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    @staticmethod
    def actualizar_producto(id, nombre, precio, categoria_id):
        Historial.historial_categorias()
        producto = Productos.query.get(id)
        if producto:
            print(f"ID: {id}, Nombre: {nombre}, Precio: {precio}, Categoria ID: {categoria_id}")
            producto.nombre = nombre
            producto.precio = precio
            if categoria_id:
                producto.fk_categoria = categoria_id
            db.session.commit()
        else:
            db.session.rollback()

    @staticmethod
    def eliminar_producto(id):
        try:
            Historial.historial_categorias()
            producto = Productos.query.get(id)
            if producto:
                producto.fk_estado = ESTADO_INACTIVO
                db.session.commit()
        except Exception as e:
            db.session.rollback()

    @staticmethod
    def activar_producto(id):
        try:
            Historial.historial_categorias()
            producto = Productos.query.get(id)
            if producto:
                categoria = Categorias.query.get(producto.fk_categoria)
                if categoria and categoria.fk_estado == ESTADO_ACTIVO:
                    producto.fk_estado = ESTADO_ACTIVO
                    db.session.commit()
                    return True
                else:
                    return False
        except Exception as e:
            db.session.rollback()
    
    @staticmethod
    def obtener_productos_disponibles():
        return Productos.query.filter(Productos.estado.has(id=ESTADO_INACTIVO)).all()