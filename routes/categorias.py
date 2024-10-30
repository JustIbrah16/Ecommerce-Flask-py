from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from services.category_queries import CategoryQueries
from flask_login import login_required

categorias = Blueprint('categorias', __name__)

@categorias.route("/add")
@login_required
def index():
    categorias = CategoryQueries.obtener_categorias()
    return render_template('categorias.html', categorias = categorias)


@categorias.route("/add", methods=['POST', 'GET'])  # Asegúrate de que solo los usuarios autenticados puedan acceder a esto
@login_required
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        estado = 2  # Ajusta según tus necesidades

        CategoryQueries.agregar_categoria(nombre, estado)
        return redirect(url_for('categorias.index'))

    return render_template('categorias.html')

@categorias.route("/update/<id>", methods=['POST', 'GET'])
@login_required
def update(id):
    categoria = CategoryQueries.buscar_categorias_por_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        CategoryQueries.actualizar_categoria(id, nombre)
        return redirect(url_for('categorias.index'))
    
    return render_template('update.html', categoria=categoria)


@categorias.route("/delete/<id>", methods=['POST'])
@login_required
def delete(id):
    CategoryQueries.eliminar_categoria(id)
    return jsonify({'success': True})

@categorias.route("/activar/<id>", methods=['POST'])
@login_required
def activar(id):
    CategoryQueries.activar_categoria(id)
    return jsonify({'success': True})

@categorias.route('/categorias/<categoria_id>/historial', methods=['GET'])
@login_required
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
