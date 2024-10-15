from utils.db import db
from sqlalchemy import column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime
from .estado import Estado

class Pedidos(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    fk_estado = db.Column(db.Integer, ForeignKey('estado.id'), nullable = False)
    total = db.Column(db.Numeric(12, 2), nullable = False)
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable = False)

    estado = relationship('Estado')

    def __init__(self, fk_estado, total, fecha):
        self.fk_estado = fk_estado
        self.total = total
        self.fecha = fecha