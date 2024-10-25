from models.usuarios import Usuarios
from flask_login import LoginManager, login_user, logout_user, login_required
from utils.db import db
from utils.hash import hash_generator, check_password

class User_queries:
    
    @staticmethod
    def registrar_usuarios(user, password, fk_rol):
        hashed_password = hash_generator(password)
        nuevo_usuario = Usuarios(username=user, password=hashed_password, fk_rol=fk_rol)
        db.session.add(nuevo_usuario)
        db.session.commit()

    @staticmethod
    def login(username, password):
        usuario = Usuarios.query.filter_by(username = username).first()
        if usuario and check_password(usuario.password.encode('utf-8'), password):
            login_user(usuario)
            return True
        return False