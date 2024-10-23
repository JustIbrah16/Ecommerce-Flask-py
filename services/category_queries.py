from models.categorias import Categorias
from utils.db import db

class CategoryQueries:
    @staticmethod
    def obtener_categorias():
        return Categorias.query.all()
    
    @staticmethod
    def buscar_categorias_por_id(categoria_id):
        return Categorias.query.get(categoria_id)
    
    @staticmethod
    def agregar_categoria(nombre):
        nueva_categoria = Categorias(nombre)
        db.session.add(nueva_categoria)
        db.session.commit()

    @staticmethod
    def actualizar_categoria(categoria_id, nombre):
        categoria = Categorias.query.get(categoria_id)
        if categoria:
            categoria.nombre = nombre
            db.session.commit()
    
    @staticmethod
    def eliminar_categoria(categoria_id):
        categoria = Categorias.query.get(categoria_id)
        if categoria:
            db.session.delete(categoria) 
            db.session.commit()  

