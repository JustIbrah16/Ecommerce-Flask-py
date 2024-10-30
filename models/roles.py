from utils.db import db

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    nombre = db.Column(db.String, nullable = False)