from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from models.productos import Productos
from .categorias import Categorias
from utils.db import db


productos = Blueprint('productos', __name__)

def obtener_categoria():
    return Categorias.query.all()

def obtener_productos():
    return Productos.query.all()

@productos.route("/index_productos")
def index():
    productos = Productos.query.filter_by(fk_estado = 2)
    categorias = obtener_categoria()
    return render_template('index.html', productos = productos, categorias = categorias)

@productos.route("/add_productos", methods = ['POST'])
def add_productos():
    nombre = request.form['nombre']
    precio = request.form['precio']
    categoria_id = request.form['categoria']
    estado = 2

    categoria = Categorias.query.get(categoria_id)
    if not categoria:
        flash('Categoria no valida', 'error')
        return redirect(url_for('main.index'))

    nuevo_producto = Productos(fk_categoria = categoria_id, nombre = nombre, precio = precio, fk_estado = estado)
    db.session.add(nuevo_producto)
    db.session.commit()

    # print(f"Nombre: {nombre}, Precio: {precio}, Categoria ID: {categoria_id}")
    return redirect(url_for('main.index'))

@productos.route("/update_productos/<id>", methods = ['POST', 'GET'])
def update_productos(id):
    producto = Productos.query.get(id)
    categorias = obtener_categoria()

    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']

        categoria_seleccionada = request.form['categoria']
        if categoria_seleccionada:
            producto.fk_categoria = categoria_seleccionada

        db.session.commit()

        return redirect(url_for('productos.index'))
    
    return render_template('update_productos.html', producto = producto, categorias = categorias)

@productos.route("/delete_productos/<id>", methods=['POST'])
def delete_productos(id):
    producto = Productos.query.get(id)
    if producto:
        producto.fk_estado = 1  
        db.session.commit()
        flash('Producto eliminado correctamente', 'success')
    else:
        flash('Producto no encontrado', 'error')
    return redirect(url_for('productos.index'))