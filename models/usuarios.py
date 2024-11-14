from utils.db import db
from sqlalchemy import column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .roles import Roles
from flask_login import UserMixin
from datetime import datetime, timedelta
from utils.hash import hash_generator, check_password

class Usuarios(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    nombres = db.Column(db.String, nullable = False)
    apellidos = db.Column(db.String, nullable = False)
    email = db.Column(db.String(100))
    username = db.Column(db.String, nullable = False)
    telefono = db.Column(db.Integer, nullable = False)
    password = db.Column(db.String, nullable = False)
    fk_rol = db.Column(db.Integer, ForeignKey('roles.id'), nullable = False)
    reset_token = db.Column(db.String(100))
    reset_token_expiration = db.Column(db.DateTime, nullable=True)

    rol = relationship('Roles', backref='usuarios')

    def __init__(self, nombres, apellidos, email, username, telefono, password, fk_rol):
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.username = username
        self.telefono = telefono
        self.password = password
        self.fk_rol = fk_rol