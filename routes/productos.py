from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.productos import Productos
from .categorias import Categorias
from utils.db import db


productos = Blueprint('productos', __name__)

@productos.route("/")
def index():
    productos = Productos.query.all()
    categorias = Categorias.query.all()
    return render_template('index.html', productos = productos, categorias = categorias)

@productos.route("/add_productos", methods = ['POST'])
def add_productos():
    nombre = request.form['nombre']
    precio = request.form['precio']
    categoria_id = request.form['categoria']

    categoria = Categorias.query.get(categoria_id)
    if not categoria:
        flash('Categoria no valida', 'error')
        return redirect(url_for('productos.index'))

    nuevo_producto = Productos(fk_categoria = categoria_id, nombre = nombre, precio = precio)
    db.session.add(nuevo_producto)
    db.session.commit()

    # print(f"Nombre: {nombre}, Precio: {precio}, Categoria ID: {categoria_id}")
    return redirect(url_for('productos.index'))