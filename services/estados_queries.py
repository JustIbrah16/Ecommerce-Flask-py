from models.estado import Estado

class Estados_queries:
    @staticmethod
    def obtener_estados():
        return Estado.query.all()