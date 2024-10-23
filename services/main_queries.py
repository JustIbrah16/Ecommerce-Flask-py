from models.productos import Productos
from models.pedidos import Pedidos
from models.estado import Estado
from models.categorias import Categorias

class MainQueries:
    @staticmethod
    def obtener_productos_activos():
        return Productos.query.filter_by(fk_estado=2).all()
    
    staticmethod
    def obtener_categorias():
        return Categorias.query.all()
    
    staticmethod
    def obtener_pedidos():
        return Pedidos.query.all()
    
    staticmethod
    def obtener_estados():
        return Estado.query.all()
    