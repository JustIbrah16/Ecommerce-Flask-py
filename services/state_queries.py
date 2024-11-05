from models.estado import Estado
from utils.db import db

class Estados_queries:
    staticmethod
    def obtener_estados():
        estados =  Estado.query.order_by(Estado.id.desc()).limit(4).all()
        return estados[::-1]