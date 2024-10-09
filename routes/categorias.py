from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.categorias import Categorias
from utils.db import db

categorias = Blueprint('categorias', __name__)
@categorias.route("/")
def index():
    categorias = Categorias.query.all()
    return render_template('index.html', categorias = categorias)

@categorias.route("/add", methods = ['POST'])
def add():
    nombre = request.form['nombre']

    nueva_categoria = Categorias(nombre)

    db.session.add(nueva_categoria)
    db.session.commit()

    return redirect(url_for('categorias.index'))

@categorias.route("/update/<id>", methods = ['POST', 'GET'])
def update(id):
    categoria = Categorias.query.get(id)
    if request.method == 'POST':
        categoria.nombre = request.form['nombre']

        db.session.commit()

        return redirect(url_for('categorias.index'))
    
    return render_template('update.html', categoria = categoria)

@categorias.route("/delete/<id>")
def delete(id):
    categoria = Categorias.query.get(id)
    db.session.delete(categoria)
    db.session.commit()

    return redirect(url_for('categorias.index'))