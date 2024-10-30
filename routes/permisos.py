from flask import Blueprint, render_template, request, redirect, url_for
from models.usuarios import Usuarios
from models.permisos import Permisos
from utils.db import db

permisos = Blueprint('permisos', __name__)

@permisos.route('/permisos')
def mostrar_tabla_permisos():  
    usuarios = Usuarios.query.all()
    return render_template('tabla_permisos.html', usuarios=usuarios)

@permisos.route('/permisos/update', methods=['POST'])
def update_permisos():
    permisos_data = request.form
    for usuario_id in permisos_data:
        permiso = Permisos.query.filter_by(usuario_id=usuario_id).first()
        if not permiso:
            permiso = Permisos(usuario_id=usuario_id)

        
        permiso.eliminar = permisos_data.get(f'eliminar_{usuario_id}') == 'on'
        permiso.activar = permisos_data.get(f'activar_{usuario_id}') == 'on'
        permiso.agregar = permisos_data.get(f'agregar_{usuario_id}') == 'on'
        permiso.actualizar = permisos_data.get(f'actualizar_{usuario_id}') == 'on'
        
        db.session.add(permiso)

    db.session.commit()
    return redirect(url_for('permisos.mostrar_tabla_permisos'))  

@permisos.route('/tabla_permisos')
def tabla_permisos():  
    usuarios = Usuarios.query.all()
    
    
    return render_template('tabla_permisos.html')
