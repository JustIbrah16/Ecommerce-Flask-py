from models.usuarios import Usuarios
from models.roles import Roles
from flask_login import login_user
from utils.db import db
from utils.hash import hash_generator, check_password

class User_queries:
    
    @staticmethod
    def registrar_usuarios(nombres, apellidos, username, telefono, password, fk_rol):
        hashed_password = hash_generator(password) 
        nuevo_usuario = Usuarios(
            nombres=nombres,
            apellidos=apellidos,
            username=username,
            telefono=telefono,
            password=hashed_password,
            fk_rol=fk_rol
        )
        db.session.add(nuevo_usuario)
        db.session.commit()


    @staticmethod
    def login(username, password):
        usuario = Usuarios.query.filter_by(username = username).first()
        if usuario and check_password(usuario.password.encode('utf-8'), password):
            login_user(usuario)
            return True
        return False
    
    @staticmethod
    def listar_usuarios(page=1, per_page=8):
        result = (
            db.session.query(
                Usuarios.nombres,
                Usuarios.apellidos,
                Usuarios.username,
                Usuarios.telefono,
                Roles.nombre
            )
        ).join(Usuarios, Usuarios.fk_rol == Roles.id).paginate(page=page, per_page=per_page, error_out=False)
        return result
    
    @staticmethod
    def verificar_usuario_existente(username):
        return db.session.query(Usuarios).filter_by(username=username).first() is not None