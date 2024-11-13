from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from services.category_queries import CategoryQueries
from flask_login import login_required
from utils.permisos import requiere_permiso

ESTADO_INACTIVO = 1
ESTADO_ACTIVO = 2

categorias = Blueprint('categorias', __name__)

@categorias.route("/add")
@login_required
@requiere_permiso('mostrar_categorias')
def index():
    page = request.args.get('page', 1, type=int)
    categorias_paginadas = CategoryQueries.obtener_categorias(page=page, per_page=6)
    total_pages = categorias_paginadas.pages
    visible_pages = list(range(max(1, page - 2), min(total_pages, page + 2) + 1))

    return render_template(
        'categorias.html', 
        categorias=categorias_paginadas.items,
        page=categorias_paginadas.page,
        total_pages=total_pages,
        visible_pages=visible_pages
    )


@categorias.route("/add", methods=['POST'])
@login_required
@requiere_permiso('agregar_categorias')
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        estado = 2  

        nueva_categoria = CategoryQueries.agregar_categoria(nombre, estado)

        if nueva_categoria:  
            return redirect(url_for('categorias.index'))
        else:
            return jsonify({'error': 'No se pudo crear la categoría.'}), 400





@categorias.route("/update/<id>", methods=['POST', 'GET'])
@login_required
@requiere_permiso('actualizar_categorias')
def update(id):
    categoria = CategoryQueries.buscar_categorias_por_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        CategoryQueries.actualizar_categoria(id, nombre)
        return redirect(url_for('categorias.index'))
    
    return render_template('update.html', categoria=categoria)


@categorias.route("/delete/<id>", methods=['POST'])
@login_required
@requiere_permiso('desactivar_categorias')
def delete(id):
    categoria = CategoryQueries.buscar_categorias_por_id(id)
    if categoria and categoria.fk_estado == ESTADO_INACTIVO:
        return jsonify({'error': 'La categoría ya está eliminada.'}), 400
    
    CategoryQueries.eliminar_categoria(id)
    return jsonify({'success': True})

@categorias.route("/activar/<id>", methods=['POST'])
@login_required
@requiere_permiso('activar_categorias')
def activar(id):
    categoria = CategoryQueries.buscar_categorias_por_id(id)
    if categoria and categoria.fk_estado == ESTADO_ACTIVO:
        return jsonify({'error': 'La categoría ya está activa.'}), 400
    
    CategoryQueries.activar_categoria(id)
    return jsonify({'success': True})

@categorias.route('/categorias/<categoria_id>/historial', methods=['GET'])
@login_required
@requiere_permiso('historial_categorias')
def obtener_historial_categorias(categoria_id):
    cambios_categoria = CategoryQueries.obtener_historial_categoria(categoria_id)

    response = [{
        'id': cambio.fk_categoria, 
        'fecha_cambio': cambio.fecha,
        'usuario': cambio.username,
        'cambio': cambio.cambio,
        'estado_antiguo': cambio.estado_antiguo_nombre,
        'estado_nuevo': cambio.estado_nuevo_nombre,
        'nombre_anterior': cambio.nombre_anterior,
        'nombre_nuevo': cambio.nombre_nuevo
    } for cambio in cambios_categoria]

    return jsonify(response)



