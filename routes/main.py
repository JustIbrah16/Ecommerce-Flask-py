from flask import Blueprint, render_template
from utils.db import db
from models.productos import Productos
from models.pedidos import Pedidos
from models.estado import Estado
from models.categorias import Categorias

main = Blueprint('main', __name__)

@main.route("/", methods = ['POST', 'GET'])
def index():
    productos = Productos.query.filter_by(fk_estado = 2)
    categorias = Categorias.query.all()
    pedidos = Pedidos.query.all()
    estados = Estado.query.all()

    return render_template('index.html', productos = productos, categorias = categorias, pedidos = pedidos, estados= estados)