from flask import Flask
from routes.categorias import categorias
from routes.productos import productos
from utils.db import db

app = Flask(__name__)

app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3307/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(categorias)
app.register_blueprint(productos)