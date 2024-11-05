from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.order_queries import OrderQueries
from services.state_queries import Estados_queries
from services.product_queries import ProductQueries
from flask_login import login_required
from utils.permisos import requiere_permiso, requiere_permiso_ajax

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
    nuevo_pedido = OrderQueries.obtener_detalles_pedido(producto, cantidad)

    OrderQueries.actualizar_total_pedido(nuevo_pedido.id, nuevo_pedido.total)
    OrderQueries.marcar_producto_inactivo(producto)

    flash(f'{cantidad} producto(s) agregado(s) al pedido', 'success')
    return redirect(url_for('productos.index'))

@pedidos.route("/filtrar_pedidos", methods=['GET', 'POST'])
@requiere_permiso_ajax('filtrar_pedido')
def filtrar_pedidos():
    estado_id = request.form.get('estado')
    fecha = request.form.get('fecha')
    
    pedidos_filtrados = OrderQueries.filtrar_pedidos(estado_id, fecha)
    estados = Estados_queries.obtener_estados()  
    productos = ProductQueries.obtener_productos_disponibles()

    return render_template('index.html', pedidos=pedidos_filtrados, estados=estados, productos = productos)

@pedidos.route("/pedidos/<id>/detalles", methods=['GET'])
@requiere_permiso('detalle_pedido')
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
@requiere_permiso('guardar_pedido')
def finalizar_compra():
    data = request.get_json()

    if not data or 'productos' not in data:
        return jsonify({'error': 'Datos de productos no válidos.'}), 400
    
    try:
        nuevo_pedido = OrderQueries.finalizar_pedido(data['productos'])

        if nuevo_pedido:
            flash('Pedido realizado con éxito', 'success')
            return jsonify({'redirect': url_for('main.index')}), 201
        else:
            return jsonify({'error': 'Error al guardar el pedido en la base de datos.'}), 500
    except Exception as e:
        print("Error al procesar la compra:", e)  
        return jsonify({'error': 'Error en el servidor: ' + str(e)}), 500


@pedidos.route('/pedido/<pedido_id>/actualizar', methods=['POST'])
@requiere_permiso_ajax('actualizar_pedido')
def actualizar_estado(pedido_id):
    pedido_actualizado = OrderQueries.actualizar_estado_pedido(pedido_id)

    if not pedido_actualizado:
        return jsonify({'success': 'Pedido no encontrado'}), 404

    return jsonify({
        'success': 'Estado actualizado correctamente!',
        'nuevo_estado': pedido_actualizado.estado.nombre 
    })



@pedidos.route('/pedidos/<pedido_id>/historial', methods=['GET'])
@requiere_permiso('historial_pedido')
def obtener_detalles_pedido(pedido_id):
    cambios_detalle = OrderQueries.detalle_cambios(pedido_id)

    response = [{
        'id': cambio.id,
        'fecha_cambio': cambio.fecha_cambio,
        'fk_estado': cambio.fk_estado,
        'username': cambio.username,
        'nombre': cambio.nombre
    } for cambio in cambios_detalle]

    return jsonify(response)

