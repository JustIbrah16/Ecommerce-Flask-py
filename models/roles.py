from utils.db import db
from sqlalchemy.orm import relationship

class Roles(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String, nullable=False)

    # Relación con la tabla intermedia Rol_permisos
    permisos = relationship('Rol_permisos', back_populates='rol', lazy='dynamic')

    def obtener_permisos(self):
        return [rol_permiso.permiso for rol_permiso in self.permisos]  
