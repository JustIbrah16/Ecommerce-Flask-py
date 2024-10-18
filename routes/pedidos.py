from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages,session, jsonify
import datetime
from models.productos import Productos
from .categorias import Categorias
from utils.db import db
from models.pedidos import Pedidos
from models.detalle_pedido import Detalle_pedido
from models.estado import Estado


pedidos = Blueprint('pedidos', __name__)

def obtener_pedidos():
    return Pedidos.query.all()

@pedidos.route('/buscar_prod_id', methods=['POST'])
def buscar_prod_id():
    data = request.get_json()
    producto = Productos.query.get(data['id_prod'])

    if producto:
        return jsonify({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': str(producto.precio)  # Asegúrate de que sea un string
        })
    return jsonify({'error': 'Producto no encontrado'}), 404


@pedidos.route("/add_to_pedido/<producto_id>", methods=['POST'])
def agregar_producto_a_pedido(producto_id):
    producto = Productos.query.get(producto_id)

    if not producto or producto.fk_estado != 2:  # Solo agregar si el producto está activo
        flash("Producto no válido o inactivo", 'error')
        return redirect(url_for('productos.index'))

    # Obtener cantidad solicitada del formulario
    cantidad = int(request.form['cantidad']) if 'cantidad' in request.form else 1
    subtotal = cantidad * float(producto.precio)

    # Crear un nuevo pedido o usar uno existente
    pedido = Pedidos(fk_estado=3, total=subtotal, fecha=datetime.datetime.utcnow())
    db.session.add(pedido)
    db.session.commit()

    # Agregar los detalles del pedido
    detalle = Detalle_pedido(fk_pedido=pedido.id, fk_producto=producto.id, fk_categoria=producto.fk_categoria, cantidad=cantidad, subtotal=subtotal)
    db.session.add(detalle)
    db.session.commit()

    # Actualizar el total del pedido
    pedido.total = subtotal
    db.session.commit()

    # Opcional: Cambiar estado del producto o hacer algo después de agregar
    producto.fk_estado = 1  # Opción: marcar como inactivo si deseas que no se vea más
    db.session.commit()

    flash(f'{cantidad} producto(s) agregado(s) al pedido', 'success')
    return redirect(url_for('productos.index'))

@pedidos.route("/filtrar_pedidos", methods=['GET', 'POST'])
def filtrar_pedidos():
    estado_id = request.form.get('estado') 
    fecha = request.form.get('fecha')  

    query = Pedidos.query

    if estado_id:
        query = query.filter(Pedidos.fk_estado == estado_id)

    if fecha:
        query = query.filter(db.func.date(Pedidos.fecha) == fecha)

    pedidos_filtrados = query.all()

    estados = Estado.query.all()  
    return render_template('index.html', pedidos=pedidos_filtrados, estados=estados)

@pedidos.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    data = request.get_json()
    
    total = sum(item['subtotal'] for item in data['productos'])
    
    nuevo_pedido = Pedidos(fk_estado=3, total=total, fecha=datetime.datetime.utcnow())
    db.session.add(nuevo_pedido)
    db.session.commit()

    for item in data['productos']:
        detalle = Detalle_pedido(
            fk_pedido=nuevo_pedido.id,
            fk_producto=item['id'],
            cantidad=item['cantidad'],
            subtotal=item['subtotal']
        )
        db.session.add(detalle)

    db.session.commit()

    flash('Pedido realizado con éxito', 'success')  # Mensaje de éxito
    return jsonify({'redirect': url_for('main.index')}), 201
