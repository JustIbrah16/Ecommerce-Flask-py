from utils.db import db
from sqlalchemy import column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, ForeignKey

class Estado(db.Model):
    __tablename__ = 'estado'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    nombre = db.Column(db.String, nullable = False)

    def __init__(self, nombre):
        self.nombre = nombre