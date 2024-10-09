from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.productos import Productos
from categorias import Categorias
from utils.db import db


productos = Blueprint('productos', __name__)

@productos.route("/")
def index():
    productos = Productos.query.all()
    categorias = Categorias.query.all()
    return render_template('index.html', productos = productos, categorias = categorias)

@productos.route("/add", methods = ['POST'])
def add():
    nombre = request.form['nombre']
    precio = request.form['precio']
    categoria = request.form['categoria']

    nuevo_producto = Productos(nombre, precio, categoria)
    db.session.add(nuevo_producto)
    db.session.commit()

    return redirect(url_for('productos.index'))

    