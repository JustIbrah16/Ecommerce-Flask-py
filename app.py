from flask import Flask
from flask_bootstrap import Bootstrap5
from routes.categorias import categorias
from routes.productos import productos
from routes.pedidos import pedidos
from routes.usuarios import usuarios
from routes.main import main
from utils.db import db
from models.usuarios import Usuarios
from flask_login import LoginManager
from routes.permisos import permisos
from flask import redirect, url_for


app = Flask(__name__)

bootstrap = Bootstrap5(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'

app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3307/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Usuarios.query.get(int(id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('usuarios.login'))

app.register_blueprint(main)
app.register_blueprint(categorias)
app.register_blueprint(productos)
app.register_blueprint(pedidos)
app.register_blueprint(usuarios)
app.register_blueprint(permisos)

