from models.estado import Estado
from utils.db import db

class Estados_queries:
    staticmethod
    def obtener_estados():
        return Estado.query.all()