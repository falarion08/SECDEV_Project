from app.models import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(13), nullable = False)
    hash = db.Column(db.String(255),nullable = False)
    salt = db.Column(db.String(255),nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    profile_picture_id = db.Column(db.Integer,db.ForeignKey('files.file_id'))
    
    def __init__(self,email,hash,salt,phone_number,full_name,profile_picture_id):
        self.email=email
        self.hash = hash
        self.salt = salt
        self.phone_number=phone_number
        self.full_name = full_name
        self.profile_picture_id = profile_picture_id
        
    def json(self):
        return {'id': self.id, 'email': self.email, 'phone_number':self.phone_number, 'full_name':self.full_name}
