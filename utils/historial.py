from sqlalchemy import text
from flask_login import current_user
from utils.db import db

class Historial:
    @staticmethod
    def historial_categorias():
        db.session.execute(text('INSERT INTO tabla_temporal (id_user) VALUES (:user_id)'), {'user_id': current_user.id})