from models.usuarios import Usuarios
from models.roles import Roles
from models.permisos import Permisos
from functools import wraps
from flask import abort
from flask_login import current_user

# Definición de la función para cargar roles y permisos
def cargar_roles():
    roles_permisos = {}
    roles = Roles.query.all()

    for rol in roles:
        permisos = [permiso.nombre for permiso in rol.permisos]  # Obtener los permisos del rol
        roles_permisos[rol.nombre] = permisos

    return roles_permisos

# Cargar los roles y permisos al inicio de la aplicación
roles_permisos = cargar_roles()

def tiene_permiso(usuario, permiso):
    rol = usuario.rol.nombre  # Obtener el nombre del rol del usuario
    return permiso in roles_permisos.get(rol, [])

def requiere_permiso(permiso):
    def decorador(func):
        @wraps(func)
        def envoltura(*args, **kwargs):
            usuario = current_user
            if not tiene_permiso(usuario, permiso):
                abort(403)  # Prohibido
            return func(*args, **kwargs)
        return envoltura
    return decorador
