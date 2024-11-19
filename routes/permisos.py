from flask import Blueprint, render_template, request, jsonify
from models.permisos import Permisos
from models.grupos import Grupos
from models.roles import Roles
from models.roles_permisos import Rol_permisos
from utils.db import db
from services.user_queries import User_queries
from utils.permisos import requiere_permiso

permisos = Blueprint('permisos', __name__)

@permisos.route('/permisos')
def mostrar_tabla_permisos():  
    pass

@requiere_permiso('mostrar_permisos')
@permisos.route('/update_permisos/<id>/permisos', methods=['GET'])
def update_permisos(id):
    rol = Roles.query.get_or_404(id)
    productos_permisos = Permisos.query.filter_by(fk_grupo = 1).all()
    categorias_permisos = Permisos.query.filter_by(fk_grupo= 2).all()
    pedidos_permisos = Permisos.query.filter_by(fk_grupo = 3).all()
    permisos = rol.obtener_permisos()
    todos_permisos = Permisos.query.all()
    return render_template('permisos.html', 
                           rol = rol, 
                           permisos = permisos, 
                           todos_permisos = todos_permisos,
                           productos_permisos = productos_permisos,
                           categorias_permisos = categorias_permisos,
                           pedidos_permisos = pedidos_permisos)

@permisos.route('/tabla_permisos')
def tabla_permisos():  
    page = request.args.get('page', 1, type=int)
    usuarios_paginados = User_queries.listar_usuarios(page=page, per_page=8)
    roles = Roles.query.all()
    total_pages = usuarios_paginados.pages
    visible_pages = list(range(max(1, page - 2), min(total_pages, page + 2) + 1))

    return render_template('tabla_permisos.html', 
                           usuarios=usuarios_paginados.items, 
                           roles=roles, 
                           page=usuarios_paginados.page, 
                           total_pages=total_pages, 
                           visible_pages=visible_pages)

@permisos.route('/roles/<int:rol_id>/permisos/asignar/<int:permiso_id>', methods=['POST'])
def asignar_permiso(rol_id, permiso_id):
    rol = Roles.query.get_or_404(rol_id)
    permiso = Permisos.query.get_or_404(permiso_id)

    existente = Rol_permisos.query.filter_by(rol_id=rol_id, permiso_id=permiso_id).first()
    if existente:
        return jsonify({"status": "error", "message": "El permiso ya está asignado a este rol."}), 400

    nuevo_rol_permiso = Rol_permisos(rol_id=rol.id, permiso_id=permiso.id)
    db.session.add(nuevo_rol_permiso)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Permiso asignado exitosamente."})


@permisos.route('/roles/<int:rol_id>/permisos/revocar/<int:permiso_id>', methods=['POST'])
def revocar_permiso(rol_id, permiso_id):
    rol_permiso = Rol_permisos.query.filter_by(rol_id=rol_id, permiso_id=permiso_id).first()
    
    if not rol_permiso:
        return jsonify({"status": "error", "message": "El permiso ya ha sido revocado de este rol."}), 400

    db.session.delete(rol_permiso)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Permiso revocado exitosamente."})

