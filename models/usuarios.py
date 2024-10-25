from utils.db import db
from sqlalchemy import column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .roles import Roles
from flask_login import UserMixin

class Usuarios(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    fk_rol = db.Column(db.Integer, ForeignKey('roles.id'), nullable = False)

    roles = relationship('Roles')

    def __init__(self, username, password, fk_rol):
        self.username = username
        self.password = password
        self.fk_rol = fk_rol