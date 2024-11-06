from models.usuarios import Usuarios
from models.roles import Roles
from models.permisos import Permisos
from functools import wraps
from flask import abort, current_app, render_template
from flask_login import current_user

# Definición de la función para cargar roles y permisos
def cargar_roles():
    roles_permisos = {}
    roles = Roles.query.all()

    for rol in roles:
        permisos = [permiso.permiso.nombre for permiso in rol.permisos]
        roles_permisos[rol.nombre] = permisos

    return roles_permisos

def tiene_permiso_filter(usuario, permiso):
    if usuario.rol is None:
        return False
    rol = usuario.rol.nombre
    roles_permisos = cargar_roles()
    return permiso in roles_permisos.get(rol, [])


def tiene_permiso(usuario, permiso):
    if usuario.rol is None:
        return False
    rol = usuario.rol.nombre
    roles_permisos = cargar_roles()
    return permiso in roles_permisos.get(rol, [])


def requiere_permiso(permiso):
    def decorador(func):
        @wraps(func)
        def envoltura(*args, **kwargs):
            usuario = current_user
            if not usuario.is_authenticated:
                abort(403)
            if not tiene_permiso(usuario, permiso):
                return render_template('403.html') # Prohibido si no tiene permiso
            return func(*args, **kwargs)
        return envoltura
    return decorador

def requiere_permiso_ajax(permiso):
    def decorador(func):
        @wraps(func)
        def envoltura(*args, **kwargs):
            usuario = current_user
            if not usuario.is_authenticated:
                return {'error': 'No estás autenticado'}, 403
            
            if not tiene_permiso(usuario, permiso):
                return {'error': 'No tienes permiso para realizar esta acción'}, 403
            
            return func(*args, **kwargs)
        return envoltura
    return decorador



