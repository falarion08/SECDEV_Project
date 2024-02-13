from app.models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(13), nullable = False)
    hash = db.Column(db.String(255),nullable = False)
    salt = db.Column(db.String(255),nullable=False)
    full_name = db.Column(db.String(120), nullable=False)

    def __init__(self,email,hash,salt,phone_number,full_name):
        self.email=email
        self.hash = hash
        self.salt = salt
        self.phone_number=phone_number
        self.full_name = full_name
        
    def json(self):
        return {'id': self.id, 'email': self.email, 'phone_number':self.phone_number, 'full_name':self.full_name}