from services.user_queries import User_queries
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user

usuarios = Blueprint('usuarios', __name__)

@usuarios.route('/register', methods = ['POST', 'GET'])
def registrar_usuarios():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fk_rol = 1
        if not username or not password:
            return redirect(url_for('usuarios.registrar_usuarios'))
        
        User_queries.registrar_usuarios(username, password, fk_rol)
        return redirect(url_for('usuarios.login'))
    
    return render_template('register.html')

@usuarios.route('/login', methods = ['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return redirect(url_for('usuarios.login'))
        
        if User_queries.login(username, password):
            return redirect(url_for('main.index'))
        else:
            return render_template('login.hmtl', error = 'Credenciales incorrectas')
    return render_template('login.html')

@usuarios.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('usuarios.login'))