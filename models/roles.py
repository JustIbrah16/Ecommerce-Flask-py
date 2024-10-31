from utils.db import db
from .roles_permisos import Rol_permisos
from sqlalchemy.orm import relationship

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    nombre = db.Column(db.String, nullable = False)

    rol_permisos = relationship('Rol_permisos', back_populates='rol')

    def obtener_permisos(self):
        return [rol_permiso.permiso for rol_permiso in self.rol_permisos]