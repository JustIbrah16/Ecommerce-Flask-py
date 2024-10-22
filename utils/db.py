from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class query():

    def filter(self, param):
        self.param = param