from models.categorias import Categorias
from models.productos import Productos
from utils.db import db
from utils.historial import Historial
from models.historial_categorias import Historial_categorias
from models.estado import Estado
from models.usuarios import Usuarios
from sqlalchemy.orm import aliased

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
    #AGREGAR CREACION 
    @staticmethod
    def obtener_historial_categoria(categoria_id):
        try:
            categoria_id = int(categoria_id)  

            estado_antiguo_alias = aliased(Estado)
            estado_nuevo_alias = aliased(Estado)

            resultado = (
                db.session.query(
                    Historial_categorias.id,  
                    Historial_categorias.fecha,
                    Usuarios.username,
                    Historial_categorias.cambio,
                    estado_antiguo_alias.nombre.label('estado_antiguo_nombre'),
                    estado_nuevo_alias.nombre.label('estado_nuevo_nombre'),
                    Historial_categorias.nombre_anterior,
                    Historial_categorias.nombre_nuevo,
                    Historial_categorias.fk_categoria  
                )
                .join(estado_antiguo_alias, Historial_categorias.estado_antiguo == estado_antiguo_alias.id)
                .join(estado_nuevo_alias, Historial_categorias.estado_nuevo == estado_nuevo_alias.id)
                .join(Usuarios, Usuarios.id == Historial_categorias.fk_user)
                .filter(Historial_categorias.fk_categoria == categoria_id)  
                .all()
            )
            
            return resultado or []
        except Exception as e:
            print(f"Error al obtener el historial de la categoría [id_categoria]: {e}")
            return []


    

