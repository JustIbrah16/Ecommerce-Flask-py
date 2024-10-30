from utils.db import db
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Historial_pedidos(db.Model):
    __tablename__ = 'historial_pedidos' 

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fk_pedido = db.Column(db.Integer, nullable=False)
    fk_user = db.Column(db.Integer, nullable=True)
    fk_estado = db.Column(db.Integer, nullable=False)
    cambio = db.Column(db.String(100), nullable=False)
    fecha_cambio = db.Column(db.TIMESTAMP, nullable=False)
    estado_antiguo = db.Column(db.Integer, nullable=False)
    estado_nuevo = db.Column(db.Integer, nullable=False)
