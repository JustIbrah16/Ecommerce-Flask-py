from flask import Blueprint, render_template
from services.main_queries import MainQueries

main = Blueprint('main', __name__)

@main.route("/", methods = ['POST', 'GET'])
def index():
    productos = MainQueries.obtener_productos_activos()
    categorias = MainQueries.obtener_categorias()
    pedidos = MainQueries.obtener_pedidos()
    estados = MainQueries.obtener_estados()

    return render_template('index.html', productos = productos, categorias = categorias, pedidos = pedidos, estados= estados)