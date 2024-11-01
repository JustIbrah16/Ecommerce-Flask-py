from flask import Blueprint, render_template, request, redirect, url_for
from models.usuarios import Usuarios
from models.permisos import Permisos
from models.roles import Roles
from models.roles_permisos import Rol_permisos
from utils.db import db
from services.user_queries import User_queries

permisos = Blueprint('permisos', __name__)

@permisos.route('/permisos')
def mostrar_tabla_permisos():  
    pass

@permisos.route('/update_permisos/<id>/permisos', methods=['GET'])
def update_permisos(id):
    rol = Roles.query.get_or_404(id)
    permisos = rol.obtener_permisos()
    todos_permisos = Permisos.query.all()
    return render_template('permisos.html', rol = rol, permisos = permisos, todos_permisos = todos_permisos)

@permisos.route('/tabla_permisos')
def tabla_permisos():  
    usuarios = User_queries.listar_usuarios()  
    roles = Roles.query.all()
    return render_template('tabla_permisos.html', usuarios=usuarios, roles = roles)

@permisos.route('/roles/<int:rol_id>/permisos/asignar/<int:permiso_id>', methods=['POST'])
def asignar_permiso(rol_id, permiso_id):
    rol = Roles.query.get_or_404(rol_id)
    permiso = Permisos.query.get_or_404(permiso_id)

    nuevo_rol_permiso = Rol_permisos(rol_id=rol.id, permiso_id=permiso.id)
    db.session.add(nuevo_rol_permiso)
    db.session.commit()

    # Redirección usando el parámetro correcto
    return redirect(url_for('permisos.update_permisos', id=rol.id))


@permisos.route('/roles/<int:rol_id>/permisos/revocar/<int:permiso_id>', methods=['POST'])
def revocar_permiso(rol_id, permiso_id):
    rol_permiso = Rol_permisos.query.filter_by(rol_id=rol_id, permiso_id=permiso_id).first_or_404()
    db.session.delete(rol_permiso)
    db.session.commit()

    return redirect(url_for('permisos.update_permisos', id=rol_id))

