from flask import Flask, session, redirect, url_for, request
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
from utils.permisos import tiene_permiso_filter
from datetime import timedelta



app = Flask(__name__)
bootstrap = Bootstrap5(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'

app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

db.init_app(app)

app.jinja_env.filters['tiene_permiso'] = tiene_permiso_filter

@login_manager.user_loader
def load_user(id):
    return Usuarios.query.get(int(id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('usuarios.login'))

@app.before_request
def make_session_permanent():
    session.permanent = True


app.register_blueprint(main)
app.register_blueprint(categorias)
app.register_blueprint(productos)
app.register_blueprint(pedidos)
app.register_blueprint(usuarios)
app.register_blueprint(permisos)

