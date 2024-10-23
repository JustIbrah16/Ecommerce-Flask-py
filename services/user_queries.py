from models.usuarios import Usuarios
from utils.db import db

class User_queries:
    
    @staticmethod
    def registrar_usuarios(user, password, fk_rol):
        nuevo_usuario = Usuarios(username=user, password=password, fk_rol=fk_rol)
        db.session.add(nuevo_usuario)
        db.session.commit()

    @staticmethod
    def login(id):
        usuario = Usuarios.query.get(id)
                