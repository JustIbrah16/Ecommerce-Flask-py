from models.categorias import Categorias
from sqlalchemy import text
from utils.db import db
from models.productos import Productos
from utils.historial import Historial
from flask_login import current_user
from models.tabla_temporal import Tabla_temporal

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

            print(f'El id de la categoria es: {nueva_categoria.id}')
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
                print(f'El ID es: {current_user.id}')
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
                categoria.fk_estado = 1
                productos = Productos.query.filter_by(fk_categoria = id).all()
                for producto in productos:
                    producto.fk_estado = 1
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
                categoria.fk_estado = 2
                productos = Productos.query.filter_by(fk_categoria = id).all()
                for producto in productos:
                    producto.fk_estado = 2
                db.session.commit()
                print('No se pudo activar la categoria')
        except Exception as e:
            db.session.rollback()

    

