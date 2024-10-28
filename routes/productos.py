from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.product_queries import ProductQueries
from models.categorias import Categorias

productos = Blueprint('productos', __name__)

def obtener_categoria():
    return Categorias.query.all()

@productos.route("/buscar_prod_id", methods=['POST'])
def buscar_prod_id():
    data = request.get_json()
    id_prod = data.get('id_prod')
    producto = ProductQueries.buscar_prod_por_id(id_prod)
    if producto:
        return jsonify(producto.to_dict())  
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

@productos.route("/add_productos")
def index():
    productos = ProductQueries.obtener_productos()
    categorias = obtener_categoria()
    return render_template('productos.html', productos=productos, categorias=categorias)

@productos.route("/add_productos", methods=['POST', 'GET'])
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
        return redirect(url_for('main.index'))
    
    return render_template('productos.html')

@productos.route("/update_productos/<id>", methods=['POST', 'GET'])
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
def delete_productos(id):
    ProductQueries.eliminar_producto(id)
    return jsonify({'success': True})

@productos.route("/activar_producto/<id>", methods=['POST'])
def activar_producto(id):
    success = ProductQueries.activar_producto(id)
    if success:
        return jsonify({'success' : True})
    else:
        return jsonify({'success': False, 'message': 'No se puede activar el producto. Active o cambie la categoria primero'})



        