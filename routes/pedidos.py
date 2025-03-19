from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from services.order_queries import OrderQueries
from services.state_queries import Estados_queries
from services.product_queries import ProductQueries
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
        return redirect(url_for('productos.index'))

    cantidad = int(request.form['cantidad']) if 'cantidad' in request.form else 1
    nuevo_pedido = OrderQueries.obtener_detalles_pedido(producto, cantidad)

    OrderQueries.actualizar_total_pedido(nuevo_pedido.id, nuevo_pedido.total)
    OrderQueries.marcar_producto_inactivo(producto)

    return redirect(url_for('productos.index'))


@pedidos.route("/filtrar_pedidos", methods=['GET', 'POST'])
@requiere_permiso_ajax('filtrar_pedido')
def filtrar_pedidos():
    estado_id = request.form.get('estado')
    fecha = request.form.get('fecha')

    page_pedidos = request.args.get('pedidos_page', 1, type=int)
    pedidos_per_page = 8
    pedidos_filtrados = OrderQueries.filtrar_pedidos(estado_id, fecha).paginate(page=page_pedidos, per_page=pedidos_per_page, error_out=False)

    page_productos = request.args.get('page', 1, type=int)
    productos_per_page = 5
    productos_paginate = ProductQueries.obtener_productos_disponibles().paginate(page=page_productos, per_page=productos_per_page, error_out=False)

    estados = Estados_queries.obtener_estados()

    return render_template(
        'index.html',
        pedidos=pedidos_filtrados.items,
        estados=estados,
        productos=productos_paginate.items,
        pagination=productos_paginate,
        pedidos_pagination=pedidos_filtrados
    )


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
            return jsonify({'redirect': url_for('main.index')}), 201
        else:
            return jsonify({'error': 'Error al guardar el pedido en la base de datos.'}), 500
    except Exception as e:
        print("Error al procesar la compra:", e)
        return jsonify({'error': 'Error en el servidor: ' + str(e)}), 500


@pedidos.route('/pedido/<pedido_id>/actualizar', methods=['POST'])
@requiere_permiso_ajax('actualizar_pedido')
def actualizar_estado(pedido_id):

    data = request.get_json()
    version_enviado = data.get('version')


    pedido_actualizado = OrderQueries.actualizar_estado_pedido(pedido_id, version_enviado)

    if not pedido_actualizado:
        return jsonify({'success': 'El pedido ha sido actualizado por otro usuario. Intenta nuevamente.'}), 409


    return jsonify({
        'success': 'Estado actualizado correctamente!',
        'nuevo_estado': pedido_actualizado.estado.nombre,
        'version': pedido_actualizado.version
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
