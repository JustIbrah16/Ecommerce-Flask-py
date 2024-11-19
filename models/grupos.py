from utils.db import db
from sqlalchemy import column, Integer, String

class Grupos(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    nombre = db.Column(db.String, nullable = False)