from . import db

class File(db.Model):
    id = db.Column(db.Integer, autoincrement=True,nullable=False,primary_key = True)