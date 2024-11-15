from flask import Blueprint, render_template, request
from services.main_queries import MainQueries
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route("/", methods = ['POST', 'GET'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    productos_paginate = MainQueries.obtener_productos_activos(page, per_page)

    page_pedidos = request.args.get('pedidos_page', 1, type=int)
    pedidos_per_page = 8
    pedidos_paginate = MainQueries.obtener_pedidos_paginados(page_pedidos, pedidos_per_page)

    categorias = MainQueries.obtener_categorias()
    estados = MainQueries.obtener_estados()
    estados_filtrados = [estado for estado in estados if estado.nombre in ["espera", "preparacion", "reparto", "entregado"]]
    return render_template('index.html', 
                           productos = productos_paginate.items, 
                           categorias = categorias, 
                           pedidos = pedidos_paginate.items, 
                           estados= estados_filtrados,
                           pagination= productos_paginate,
                           pedidos_pagination = pedidos_paginate)