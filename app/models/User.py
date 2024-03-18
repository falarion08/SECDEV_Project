from flask_login import UserMixin
from . import db,Workspace,WorkspaceMembers


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(13), nullable = False)
    hash = db.Column(db.String(255),nullable = False)
    salt = db.Column(db.String(255),nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    profile_picture = db.Column(db.String(), nullable=True)
    role = db.Column(db.String(50), nullable=False)
    workspaces = db.relationship('Workspace', backref='owner')
    workspaces_member_of = db.relationship('WorkspaceMembers', backref = 'member_details')

    def __init__(self, email, hash, salt, phone_number, full_name, profile_picture, role):
        self.email=email
        self.hash = hash
        self.salt = salt
        self.phone_number=phone_number
        self.full_name = full_name
        self.profile_picture = profile_picture
        self.role = role

    def json(self):
        return {'id': self.id, 'email': self.email, 'phone_number':self.phone_number, 'full_name':self.full_name}

