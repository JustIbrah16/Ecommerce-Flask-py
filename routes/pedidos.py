from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import datetime
from models.productos import Productos
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
            'precio': str(producto.precio)  
        })
    return jsonify({'error': 'Producto no encontrado'}), 404

@pedidos.route("/add_to_pedido/<producto_id>", methods=['POST'])
def agregar_producto_a_pedido(producto_id):
    producto = Productos.query.get(producto_id)

    if not producto or producto.fk_estado != 2: 
        flash("Producto no válido o inactivo", 'error')
        return redirect(url_for('productos.index'))

    
    cantidad = int(request.form['cantidad']) if 'cantidad' in request.form else 1
    subtotal = cantidad * float(producto.precio)

    
    pedido = Pedidos(fk_estado=3, total=subtotal, fecha=datetime.datetime.utcnow())
    db.session.add(pedido)
    db.session.commit()

   
    detalle = Detalle_pedido(fk_pedido=pedido.id, fk_producto=producto.id, fk_categoria=producto.fk_categoria, cantidad=cantidad, subtotal=subtotal)
    db.session.add(detalle)
    db.session.commit()

    
    pedido.total = subtotal
    db.session.commit()

    
    producto.fk_estado = 1  
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

    flash('Pedido realizado con éxito', 'success')  
    return jsonify({'redirect': url_for('main.index')}), 201


@pedidos.route('/pedido/<pedido_id>/actualizar', methods=['POST'])
def actualizar_estado(pedido_id):
    
    pedido = Pedidos.query.get(pedido_id) 
    
    if not pedido:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('main.index'))
    
    
    estado_actual = pedido.fk_estado
    
    pedido.fk_estado = estado_actual + 1
    
    
    db.session.commit()
    
    flash('Estado del pedido actualizado', 'success')
    return redirect(url_for('main.index'))
