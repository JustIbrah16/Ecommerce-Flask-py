from services.user_queries import User_queries
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import  logout_user
import re


usuarios = Blueprint('usuarios', __name__)

def validar_contraseña(password):
    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
    return bool(re.match(regex, password))

@usuarios.route('/register', methods=['POST', 'GET'])
def registrar_usuarios():
    if request.method == 'POST':
        nombres = request.form['nombre']
        apellidos = request.form['apellido']
        email = request.form['email']
        username = request.form['username']
        telefono = request.form['telefono']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        fk_rol = 3  

        
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$", nombres):
            flash("El nombre solo debe contener letras y espacios.", "danger")
            return render_template('register.html')

    
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$", apellidos):
            flash("El apellido solo debe contener letras y espacios.", "danger")
            return render_template('register.html')

       
        if not re.match(r"^(?=.*[A-Za-z])[A-Za-z0-9]+$", username):
            flash("El nombre de usuario debe contener letras y puede incluir números, sin caracteres especiales.", "danger")
            return render_template('register.html')

        
        if not re.match(r"^\+?[0-9]+$", telefono):
            flash("El número de teléfono solo debe contener números y puede iniciar con '+'.", "danger")
            return render_template('register.html')

        
        if not validar_contraseña(password):
            flash("La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una minúscula, un número y un carácter especial.", "danger")
            return render_template('register.html')
        
        if password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return render_template('register.html')
        
        
        User_queries.registrar_usuarios(nombres, apellidos, email, username, telefono, password, fk_rol)
        flash("Usuario registrado exitosamente.", "success")
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

# @usuarios.route('/permisos')
# def permisos():
#     usuarios = Usuarios.query.all()  
#     acciones = ["Agregar", "Eliminar", "Activar", "Actualizar"]  
#     return render_template('tabla_permisos.html', usuarios=usuarios, acciones=acciones)