from utils.db import db
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .usuarios import Usuarios

class Permisos(db.Model):
    __tablename__ = 'permisos'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    eliminar = Column(Boolean, default=False)
    activar = Column(Boolean, default=False)
    agregar = Column(Boolean, default=False)
    actualizar = Column(Boolean, default=False)

    usuario = relationship('Usuarios', backref='permisos')

    def __init__(self, usuario_id, eliminar=False, activar=False, agregar=False, actualizar=False):
        self.usuario_id = usuario_id
        self.eliminar = eliminar
        self.activar = activar
        self.agregar = agregar
        self.actualizar = actualizar
