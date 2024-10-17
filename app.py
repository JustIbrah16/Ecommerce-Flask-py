from flask import Flask
from flask_bootstrap import Bootstrap5
from routes.categorias import categorias
from routes.productos import productos
from routes.pedidos import pedidos
from routes.main import main
from utils.db import db

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(main)
app.register_blueprint(categorias)
app.register_blueprint(productos)
app.register_blueprint(pedidos)