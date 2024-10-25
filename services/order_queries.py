from models.pedidos import Pedidos
from models.detalle_pedido import Detalle_pedido
from models.productos import Productos
from models.estado import Estado
from utils.db import db
import datetime

class OrderQueries:
    @staticmethod
    def obtener_pedidos():
        return Pedidos.query.all()

    @staticmethod
    def buscar_producto_por_id(id_prod):
        return Productos.query.get(id_prod)

    @staticmethod
    def agregar_pedido_y_detalle(producto, cantidad):
        subtotal = cantidad * float(producto.precio)
        nuevo_pedido = Pedidos(fk_estado=3, total=subtotal, fecha=datetime.datetime.utcnow())
        
        db.session.add(nuevo_pedido)
        db.session.commit()

        detalle = Detalle_pedido(fk_pedido=nuevo_pedido.id, fk_producto=producto.id, fk_categoria=producto.fk_categoria, cantidad=cantidad, subtotal=subtotal)
        db.session.add(detalle)
        db.session.commit()

        return nuevo_pedido

    @staticmethod
    def actualizar_total_pedido(pedido_id, subtotal):
        pedido = Pedidos.query.get(pedido_id)
        if pedido:
            pedido.total = subtotal
            db.session.commit()

    @staticmethod
    def marcar_producto_inactivo(producto):
        producto.fk_estado = 1
        db.session.commit()

    @staticmethod
    def filtrar_pedidos(estado_id=None, fecha=None):
        query = Pedidos.query
        if estado_id:
            query = query.filter(Pedidos.fk_estado == estado_id)
        if fecha:
            query = query.filter(db.func.date(Pedidos.fecha) == fecha)
        return query.all()

    @staticmethod
    def obtener_detalles_pedido(pedido_id):
        return (Detalle_pedido.query
                .join(Productos)
                .filter(Detalle_pedido.fk_pedido == pedido_id)
                .add_columns(Productos.nombre, Productos.precio, Detalle_pedido.cantidad, Detalle_pedido.subtotal)
                .all())

    @staticmethod
    def finalizar_pedido(productos):
        total = sum(item['subtotal'] for item in productos)
        nuevo_pedido = Pedidos(fk_estado=3, total=total, fecha=datetime.datetime.utcnow())
        
        db.session.add(nuevo_pedido)
        db.session.commit()

        for item in productos:
            detalle = Detalle_pedido(
                fk_pedido=nuevo_pedido.id,
                fk_producto=item['id'],
                cantidad=item['cantidad'],
                subtotal=item['subtotal']
            )
            db.session.add(detalle)
        db.session.commit()

        return nuevo_pedido

    @staticmethod
    def actualizar_estado_pedido(pedido_id):
        pedido = Pedidos.query.get(pedido_id)
        if pedido:
            pedido.fk_estado += 1
            db.session.commit()
            return pedido
        return None