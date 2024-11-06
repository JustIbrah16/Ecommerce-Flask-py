from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.product_queries import ProductQueries
from models.categorias import Categorias
from flask_login import login_required
from utils.permisos import requiere_permiso, requiere_permiso_ajax

productos = Blueprint('productos', __name__)

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
    productos = ProductQueries.obtener_productos()
    categorias = obtener_categoria()
    return render_template('productos.html', productos=productos, categorias=categorias)

@productos.route("/add_productos", methods=['POST', 'GET'])
@login_required
@requiere_permiso('agregar_productos')
def add_productos():
    if request.method == 'POST':    
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria_id = request.form['categoria']
        estado = 2

        categoria = Categorias.query.get(categoria_id)
        if not categoria:
            flash('Categoria no valida', 'error')
            return redirect(url_for('main.index'))

        ProductQueries.agregar_producto(nombre, precio, categoria_id, estado)
        return redirect(url_for('productos.index'))
    
    return render_template('productos.html')

@productos.route("/update_productos/<id>", methods=['POST', 'GET'])
@login_required
@requiere_permiso('actualizar_productos')
def update_productos(id):
    producto = ProductQueries.buscar_prod_por_id(id)
    categorias = obtener_categoria()

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
    ProductQueries.eliminar_producto(id)
    return jsonify({'success': True})

@productos.route("/activar_producto/<id>", methods=['POST'])
@login_required
@requiere_permiso('activar_productos')
def activar_producto(id):
    success = ProductQueries.activar_producto(id)
    if success:
        return jsonify({'success' : True})
    else:
        return jsonify({'success': False, 'message': 'No se puede activar el producto. Active o cambie la categoria primero'})


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