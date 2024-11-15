from models.productos import Productos
from models.pedidos import Pedidos
from models.estado import Estado
from models.categorias import Categorias

ESTADO_INACTIVO = 1
ESTADO_ACTIVO = 2
class MainQueries:
    @staticmethod
    def obtener_productos_activos(page, per_page):
        return Productos.query.filter_by(fk_estado=ESTADO_ACTIVO).paginate(page=page, per_page=per_page, error_out=False)
    
    staticmethod
    def obtener_categorias():
        return Categorias.query.all()
    
    staticmethod
    def obtener_pedidos_paginados(page, per_page):
        return Pedidos.query.paginate(page = page, per_page=8, error_out=False)
    
    staticmethod
    def obtener_estados():
        return Estado.query.all()