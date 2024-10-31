from models.productos import Productos
from models.categorias import Categorias
from utils.db import db
from utils.historial import Historial
from models.historial_productos import Historial_producto
from models.estado import Estado
from models.usuarios import Usuarios
from sqlalchemy.orm import aliased
from sqlalchemy import case, label



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
    
  

    @staticmethod
    def obtener_historial_producto(producto_id):
        try:
            estado_antiguo_alias = aliased(Estado)
            estado_nuevo_alias = aliased(Estado)
            categoria_antigua_alias = aliased(Categorias)
            categoria_actual_alias = aliased(Categorias)

            resultado = (
                db.session.query(
                    Historial_producto.id,
                    Historial_producto.fecha,
                    Usuarios.username,
                    Historial_producto.cambio,
                    estado_antiguo_alias.nombre.label('estado_antiguo_nombre'),
                    estado_nuevo_alias.nombre.label('estado_nuevo_nombre'),
                    Historial_producto.nombre_anterior,
                    Historial_producto.nombre_nuevo,
                    Historial_producto.precio_antiguo,
                    Historial_producto.precio_actual,
                    categoria_antigua_alias.nombre.label('categoria_antigua_nombre'),
                    categoria_actual_alias.nombre.label('categoria_actual_nombre'),
                    Historial_producto.fk_producto
                )
                .join(estado_antiguo_alias, Historial_producto.estado_antiguo == estado_antiguo_alias.id, isouter=True)
                .join(estado_nuevo_alias, Historial_producto.estado_nuevo == estado_nuevo_alias.id, isouter=True)
                .join(categoria_antigua_alias, Historial_producto.categoria_antigua == categoria_antigua_alias.id, isouter=True)
                .join(categoria_actual_alias, Historial_producto.categoria_actual == categoria_actual_alias.id, isouter=True)
                .join(Usuarios, Usuarios.id == Historial_producto.fk_user, isouter=True)
                .filter(Historial_producto.fk_producto == producto_id)
                .order_by(Historial_producto.fecha)
                .all()
            )

            return resultado or []
        except Exception as e:
            print(f"Error al obtener el historial del producto [id_producto]: {e}")
            return []


