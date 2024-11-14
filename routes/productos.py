from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from services.product_queries import ProductQueries
from models.categorias import Categorias
from flask_login import login_required
from utils.permisos import requiere_permiso

productos = Blueprint('productos', __name__)

ESTADO_INACTIVO = 1
ESTADO_ACTIVO = 2

def obtener_categoria():
    return Categorias.query.all()

@productos.route("/buscar_prod_id", methods=['POST'])
@login_required
def buscar_prod_id():
    data = request.get_json()
    id_prod = data.get('id_prod')
    producto = ProductQueries.buscar_prod_por_id(id_prod)
    if producto:
        return jsonify(producto.to_dict())  
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

@productos.route("/add_productos")
@login_required
@requiere_permiso('mostrar_productos')
def index():
    page = request.args.get('page', 1, type=int)
    productos_paginados = ProductQueries.obtener_productos(page=page, per_page=8)
    categorias = ProductQueries.obtener_categorias_activas()
    total_pages = productos_paginados.pages
    visible_pages = list(range(max(1, page - 2), min(total_pages, page + 2) + 1))

    return render_template(
        'productos.html', 
        productos=productos_paginados.items, 
        categorias=categorias, 
        page=productos_paginados.page, 
        total_pages=total_pages,
        visible_pages=visible_pages
    )

@productos.route("/add_productos", methods=['POST', 'GET'])
@login_required
@requiere_permiso('agregar_productos')
def add_productos():
    if request.method == 'POST':    
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria_id = request.form['categoria']
        estado = 2
        
        try:
            ProductQueries.agregar_producto(nombre, precio, categoria_id, estado)
            return redirect(url_for('productos.index'))
        except ValueError as ve:
            return redirect(url_for('productos.index', error = str(ve)))
    categorias = ProductQueries.obtener_categorias_activas()
    return render_template('productos.html', categorias=categorias)

@productos.route("/update_productos/<id>", methods=['POST', 'GET'])
@login_required
@requiere_permiso('actualizar_productos')
def update_productos(id):
    producto = ProductQueries.buscar_prod_por_id(id)
    categorias = ProductQueries.obtener_categorias_activas()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria_id = request.form['categoria']
        ProductQueries.actualizar_producto(id, nombre, precio, categoria_id)

        return redirect(url_for('productos.index'))
    
    return render_template('update_productos.html', producto=producto, categorias=categorias)

@productos.route("/delete_productos/<id>", methods=['POST'])
@login_required
@requiere_permiso('desactivar_productos')
def delete_productos(id):
    producto = ProductQueries.obtener_producto(id)
    if producto:
        categoria = Categorias.query.get(producto.fk_categoria)

        if categoria and categoria.fk_estado == ESTADO_ACTIVO:
            ProductQueries.eliminar_producto(id)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': "No se puede eliminar el producto si la categoria no está activa"})
    else:
        return jsonify({'success': False, 'message': 'Producto no encontrado'})
    

@productos.route("/activar_producto/<id>", methods=['POST'])
@login_required
@requiere_permiso('activar_productos')
def activar_producto(id):
    producto = ProductQueries.obtener_producto(id)
    if producto:
        categoria = Categorias.query.get(producto.fk_categoria)
        if categoria and categoria.fk_estado == ESTADO_ACTIVO:
            success = ProductQueries.activar_producto(id)
            if success:
                return jsonify({'success' : True})
            else:
                return jsonify({'success': False, 'message': 'No se puede activar el producto.'})
        else:
            return jsonify({'success': False, 'message': 'No se puede activar el producto si la categoría no está activa.'})
    else:
        return jsonify({'success': False, 'message': 'Producto no encontrado.'})


@productos.route('/productos/<producto_id>/historial', methods=['GET'])
@login_required
@requiere_permiso('historial_productos')
def obtener_historial_productos(producto_id):
    cambios_producto = ProductQueries.obtener_historial_producto(producto_id)

    response = [{
        'id': producto_id,
        'fecha_cambio': cambio.fecha,
        'usuario': cambio.username,
        'cambio': cambio.cambio if cambio.cambio else 'creación',
        'estado_antiguo': cambio.estado_antiguo_nombre,
        'estado_nuevo': cambio.estado_nuevo_nombre,
        'nombre_anterior': cambio.nombre_anterior,
        'nombre_nuevo': cambio.nombre_nuevo,
        'precio_antiguo': cambio.precio_antiguo,
        'precio_actual': cambio.precio_actual,
        'categoria_antigua': cambio.categoria_antigua_nombre,
        'categoria_actual': cambio.categoria_actual_nombre
    } for cambio in cambios_producto]

    return jsonify(response)

