from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from services.category_queries import CategoryQueries

categorias = Blueprint('categorias', __name__)

@categorias.route("/add")
def index():
    categorias = CategoryQueries.obtener_categorias()
    return render_template('categorias.html', categorias = categorias)

@categorias.route("/add", methods = ['POST', 'GET'])
def add():
    if request.method == 'POST':

        nombre = request.form['nombre']

        CategoryQueries.agregar_categoria(nombre)
        return redirect(url_for('categorias.index'))

    return render_template('categorias.html')

@categorias.route("/update/<id>", methods = ['POST', 'GET'])
def update(id):
    categoria = CategoryQueries.buscar_categorias_por_id(id)
    if request.method == 'POST':
        nombre =  request.form['nombre']
        CategoryQueries.actualizar_categoria(id, nombre)
        return redirect(url_for('categorias.index'))
    
    return render_template('update.html', categoria = categoria)

@categorias.route("/delete/<id>", methods=['POST'])
def delete(id):
    CategoryQueries.eliminar_categoria(id)
    return jsonify({'success': True})

@categorias.route("/activar/<id>", methods=['POST'])
def activar(id):
    CategoryQueries.activar_categoria(id)
    return jsonify({'success': True})