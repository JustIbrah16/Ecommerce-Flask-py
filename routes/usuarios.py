from services.user_queries import User_queries
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user
from models.usuarios import Usuarios
import re
usuarios = Blueprint('usuarios', __name__)

def validar_contraseña(password):
    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
    return bool(re.match(regex, password))

@usuarios.route('/register', methods = ['POST', 'GET'])
def registrar_usuarios():
    if request.method == 'POST':
        nombres = request.form['nombre']
        apellidos = request.form['apellido']
        username = request.form['username']
        telefono = request.form['telefono']
        password = request.form['password']
        fk_rol = 3
        if not username or not password:
            return redirect(url_for('usuarios.registrar_usuarios'))
        
        if not validar_contraseña(password):
            return render_template('register.html', error = 'La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una minúscula, un número y un carácter especial')
        
        User_queries.registrar_usuarios(nombres, apellidos, username, telefono, password, fk_rol)
        return redirect(url_for('usuarios.login'))
    
    return render_template('register.html')

@usuarios.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Por favor, completa ambos campos.', 'warning')
            return redirect(url_for('usuarios.login'))
        
        if User_queries.login(username, password):
            return redirect(url_for('main.index', show_modal='bienvenida'))
        else:
            flash('Usuario o contraseña incorrecta. Inténtalo de nuevo.', 'danger')
            return redirect(url_for('usuarios.login'))
    
    return render_template('login.html')

@usuarios.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('usuarios.login', show_modal = 'despedida'))

@usuarios.route('/permisos')
def permisos():
    usuarios = Usuarios.query.all()  
    acciones = ["Agregar", "Eliminar", "Activar", "Actualizar"]  
    return render_template('tabla_permisos.html', usuarios=usuarios, acciones=acciones)