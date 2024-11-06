from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from services.category_queries import CategoryQueries
from flask_login import login_required
from utils.permisos import requiere_permiso, requiere_permiso_ajax

categorias = Blueprint('categorias', __name__)

@categorias.route("/add")
@login_required
@requiere_permiso('mostrar_categorias')
def index():
    categorias = CategoryQueries.obtener_categorias()
    return render_template('categorias.html', categorias = categorias)


@categorias.route("/add", methods=['POST'])
@login_required
@requiere_permiso_ajax('agregar_categorias')
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        estado = 2  

        nueva_categoria = CategoryQueries.agregar_categoria(nombre, estado)

        if nueva_categoria:  
            return jsonify({
                'success': 'Categoría agregada con éxito!',
                'categoria': {
                    'id': nueva_categoria.id,
                    'nombre': nueva_categoria.nombre,
                    'estado': nueva_categoria.fk_estado
                }
            })
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
    CategoryQueries.eliminar_categoria(id)
    return jsonify({'success': True})

@categorias.route("/activar/<id>", methods=['POST'])
@login_required
@requiere_permiso('activar_categorias')
def activar(id):
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


