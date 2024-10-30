from utils.db import db
from sqlalchemy import column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

class Tabla_temporal(db.Model):
    __tablename__ = 'tabla_temporal'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    id_user = db.Column(db.Integer, nullable = False)