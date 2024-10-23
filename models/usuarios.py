from utils.db import db
from sqlalchemy import column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .roles import Roles

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.column(db.String, nullable = False)
    password = db.column(db.String, nullable = False)
    fk_rol = db.Column(db.Integer, ForeignKey('roles.id', nullable = False))

    roles = relationship('Roles')

    def __init__(self, username, password):
        self.username = username
        self.password = password