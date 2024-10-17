from flask import Blueprint, render_template
from utils.db import db
from .productos import obtener_productos
from .categorias import obtener_categorias
from .pedidos import obtener_pedidos
from models.productos import Productos

main = Blueprint('main', __name__)

@main.route("/")
def index():
    productos = obtener_productos()
    categorias = obtener_categorias()
    pedidos = obtener_pedidos()
    return render_template('index.html', productos = productos, categorias = categorias, pedidos = pedidos)