from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.order_queries import OrderQueries
from services.state_queries import Estados_queries
from services.product_queries import ProductQueries

pedidos = Blueprint('pedidos', __name__)

@pedidos.route('/buscar_prod_id', methods=['POST'])
def buscar_prod_id():
    data = request.get_json()
    producto = OrderQueries.buscar_producto_por_id(data['id_prod'])

    if producto:
        return jsonify({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': str(producto.precio)  
        })
    return jsonify({'error': 'Producto no encontrado'}), 404

@pedidos.route("/add_to_pedido/<producto_id>", methods=['POST'])
def agregar_producto_a_pedido(producto_id):
    producto = OrderQueries.buscar_producto_por_id(producto_id)

    if not producto or producto.fk_estado != 2:
        flash("Producto no válido o inactivo", 'error')
        return redirect(url_for('productos.index'))

    cantidad = int(request.form['cantidad']) if 'cantidad' in request.form else 1
    nuevo_pedido = OrderQueries.agregar_pedido_y_detalle(producto, cantidad)

    OrderQueries.actualizar_total_pedido(nuevo_pedido.id, nuevo_pedido.total)
    OrderQueries.marcar_producto_inactivo(producto)

    flash(f'{cantidad} producto(s) agregado(s) al pedido', 'success')
    return redirect(url_for('productos.index'))

@pedidos.route("/filtrar_pedidos", methods=['GET', 'POST'])
def filtrar_pedidos():
    estado_id = request.form.get('estado')
    fecha = request.form.get('fecha')
    
    pedidos_filtrados = OrderQueries.filtrar_pedidos(estado_id, fecha)
    estados = Estados_queries.obtener_estados()  
    productos = ProductQueries.obtener_productos_disponibles()

    return render_template('index.html', pedidos=pedidos_filtrados, estados=estados, productos = productos)

@pedidos.route("/pedidos/<id>/detalles", methods=['GET'])
def detalle_pedido(id):
    detalles = OrderQueries.obtener_detalles_pedido(id)

    resultados = [{
        'nombre': detalle.nombre,
        'precio': detalle.precio,
        'cantidad': detalle.cantidad,
        'subtotal': detalle.subtotal
    } for detalle in detalles]

    return jsonify(resultados)

@pedidos.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    data = request.get_json()
    nuevo_pedido = OrderQueries.finalizar_pedido(data['productos'])

    flash('Pedido realizado con éxito', 'success')
    return jsonify({'redirect': url_for('main.index')}), 201

@pedidos.route('/pedido/<pedido_id>/actualizar', methods=['POST'])
def actualizar_estado(pedido_id):
    pedido_actualizado = OrderQueries.actualizar_estado_pedido(pedido_id)

    if not pedido_actualizado:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('main.index'))

    
    return redirect(url_for('main.index'))
