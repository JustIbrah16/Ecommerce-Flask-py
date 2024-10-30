from models.categorias import Categorias
from models.productos import Productos
from utils.db import db
from utils.historial import Historial

ESTADO_INACTIVO = 1
ESTADO_ACTIVO = 2
class CategoryQueries:
    
    @staticmethod
    def obtener_categorias():
        return Categorias.query.all()
    
    @staticmethod
    def buscar_categorias_por_id(categoria_id):
        return Categorias.query.get(categoria_id)

    @staticmethod
    def agregar_categoria(nombre, estado):
        try:
            Historial.historial_categorias()
            nueva_categoria = Categorias(nombre=nombre, fk_estado=estado)
            db.session.add(nueva_categoria)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'Ocurrió un error: {e}')

    @staticmethod
    def actualizar_categoria(categoria_id, nombre):
        if not nombre:
            print('El nombre no puede estar vacío.')
            return False

        try:
            Historial.historial_categorias()           
            categoria = Categorias.query.get(categoria_id)
            if categoria:
                categoria.nombre = nombre
                db.session.commit()
                return True
            else:
                print('Categoría no encontrada.')
                return False
        except Exception as e:
            db.session.rollback()
            print(f'Ocurrió un error: {e}')
            return False
  
    @staticmethod
    def eliminar_categoria(id):
        try:
            Historial.historial_categorias()
            categoria = Categorias.query.get(id)
            if categoria:
                categoria.fk_estado = ESTADO_INACTIVO
                productos = Productos.query.filter_by(fk_categoria = id).all()
                for producto in productos:
                    producto.fk_estado = ESTADO_INACTIVO
                db.session.commit()  
                print('No se puedo desactivar la categoria')
        except Exception as e:
            db.session.rollback()
            print(f'Ocurrio un error: {e}')
    
    @staticmethod
    def activar_categoria(id):
        try:
            Historial.historial_categorias()
            categoria = Categorias.query.get(id)
            if categoria:
                categoria.fk_estado = ESTADO_ACTIVO
                productos = Productos.query.filter_by(fk_categoria = id).all()
                for producto in productos:
                    producto.fk_estado = ESTADO_ACTIVO
                db.session.commit()
                print('No se pudo activar la categoria')
        except Exception as e:
            db.session.rollback()

    

