from services.user_queries import User_queries
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

usuarios = Blueprint('usuarios', __name__)

@usuarios.route('/register', methods = ['POST', 'GET'])
def registrar_usuarios():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fk_rol = 1
        if username is None and password is None:
            return redirect(url_for('usuarios.registrar_usuarios'))
        
        User_queries.registrar_usuarios(username, password, fk_rol)
        return redirect(url_for('usuarios.registrar_usuarios'))
    
    return render_template('register.html')

@usuarios.route('/login', methods = ['POST', 'GET'])
def login(id):
    usuario = User_queries.login(id)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username is None and password is None:
            return redirect(url_for('usuarios.login'))
        
        User_queries