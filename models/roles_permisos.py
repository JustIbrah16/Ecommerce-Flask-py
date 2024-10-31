from utils.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Rol_permisos(db.Model):
    __tablename__ = 'rol_permisos'

    rol_id = db.Column(db.Integer, ForeignKey('roles.id'), primary_key=True, nullable=False)
    permiso_id = db.Column(db.Integer, ForeignKey('permisos.id'), primary_key=True, nullable=False)

    rol = relationship('Roles', back_populates='rol_permisos') 
    permiso = relationship('Permisos', backref='rol_permisos')  
