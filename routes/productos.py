from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from services.product_queries import ProductQueries
from models.categorias import Categorias
from models.usuarios import Usuarios
from flask_login import login_required
from utils.permisos import requiere_permiso
from flask_login import current_user
from models.productos import Productos
from utils.permisos import tiene_permiso_filter

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

@productos.route("/add_productos", methods=['POST'])
@login_required
@requiere_permiso('agregar_productos')
def add_productos():
    if request.method == 'POST':    
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria_id = request.form['categoria']
        estado = ESTADO_ACTIVO
        
        try:
            nuevo_producto = ProductQueries.agregar_producto(nombre, precio, categoria_id, estado)
            if nuevo_producto:
                return redirect(url_for('productos.index'))
            else:
                return jsonify({'error': f'El producto {nombre} ya existe'}), 400
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400

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
        if producto.fk_estado == ESTADO_INACTIVO:
            return jsonify({'success': False, 'message': 'El producto ya fue desactivado.'})
        
        categoria = Categorias.query.get(producto.fk_categoria)
        if categoria and categoria.fk_estado == ESTADO_ACTIVO:
            ProductQueries.eliminar_producto(id)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'No se puede eliminar el producto si la categoría no está activa.'})
    else:
        return jsonify({'success': False, 'message': 'Producto no encontrado.'})
    

@productos.route("/activar_producto/<id>", methods=['POST'])
@login_required
@requiere_permiso('activar_productos')
def activar_producto(id):
    producto = ProductQueries.obtener_producto(id)
    if producto:
        if producto.fk_estado == ESTADO_ACTIVO:
            return jsonify({'success': False, 'message': 'El producto ya fue activado.'})

        categoria = Categorias.query.get(producto.fk_categoria)
        if categoria and categoria.fk_estado == ESTADO_ACTIVO:
            success = ProductQueries.activar_producto(id)
            if success:
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'No se pudo activar el producto.'})
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

@productos.route("/buscar_productos", methods=["GET"])
@login_required
def buscar_productos():
    try:
        nombre = request.args.get("nombre", "").strip()
        categoria = request.args.get("categoria", "").strip()

        query = Productos.query.join(
            Categorias, Productos.fk_categoria == Categorias.id, isouter=True
        ).add_columns(
            Productos.id.label("id"),
            Productos.nombre.label("nombre"),
            Productos.precio.label("precio"),
            Categorias.nombre.label("categoria"),
            Productos.fk_estado.label("estado"),
        )
        if nombre:
            query = query.filter(Productos.nombre.ilike(f"%{nombre}%"))
        if categoria:
            query = query.filter(Categorias.nombre.ilike(f"%{categoria}%"))

        productos = query.all()
        resultados = []
        
        for p in productos:
            tiene_permiso_actualizar = tiene_permiso_filter(current_user, 'actualizar_productos')
            tiene_permiso_eliminar = tiene_permiso_filter(current_user, 'desactivar_productos')
            tiene_permiso_activar = tiene_permiso_filter(current_user, 'activar_productos')
            tiene_permiso_historial = tiene_permiso_filter(current_user, 'historial_productos')

            botones = {
                "detalle": url_for('productos.obtener_historial_productos', producto_id=p.id) if tiene_permiso_historial else None,
                "actualizar": url_for('productos.update_productos', id=p.id) if tiene_permiso_actualizar else None,
                "eliminar_activar": None
            }
            
            if tiene_permiso_eliminar and p.estado == ESTADO_ACTIVO:
                botones["eliminar_activar"] = url_for('productos.delete_productos', id=p.id)
            elif tiene_permiso_activar and p.estado == ESTADO_INACTIVO:
                botones["eliminar_activar"] = url_for('productos.activar_producto', id=p.id)
            
            resultados.append({
                "id": p.id,
                "nombre": p.nombre,
                "precio": p.precio,
                "categoria": p.categoria or "Sin categoría",
                "estado": "Activo" if p.estado == ESTADO_ACTIVO else "Inactivo",
                "botones": botones
            })

        return jsonify(resultados), 200
    except Exception as e:
        print(f"Error en buscar_productos: {e}")
        return jsonify({"error": "Error al buscar productos."}), 500

