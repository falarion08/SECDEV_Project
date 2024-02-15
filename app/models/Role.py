from app.models import db

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), autoincrement = True, primary_key = True, nullable = False, unique = True)
    role_name = db.Column(db.String(25), nullable = False,unique=True)