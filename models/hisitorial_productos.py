from utils.db import db
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Hsitorial_producto(db.Model):
    __tablename__ = 'historial_productos'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fk_producto = db.Column(db.Integer, nullable=False)
    fk_user = db.Column(db.Integer, nullable=True)
    cambio = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.TIMESTAMP, nullable=False)
    estado_antiguo = db.Column(db.Integer, nullable=False)
    estado_nuevo = db.Column(db.Integer, nullable=False)
    nombre_anterior = db.Column(db.String, nullable=False)
    nombre_nuevo = db.Column(db.String, nullable=False)