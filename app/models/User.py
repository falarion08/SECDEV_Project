from flask_login import UserMixin
from . import db,Workspace,WorkspaceMembers,Task,TaskUpdates


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
    
    # Create a one-to-many relationship with Workspace model and put an invisible columns 'owner' to the workspace model and 'workspaces' in the User model accessible only via python
    # Calling this attribute will show the workspaces owned by a user (ADMIN ONLY)
    workspaces = db.relationship('Workspace', backref='owner')
    
    # Create a one-to-many relationship with WorkspaceMembers model and put an invisible columns 'member_details' to the workspace model and 'workspace_member_of'in the User Model accessible only via flask
    # Calling this attribute will return an array of all workspaces the users are a member of 
    workspaces_member_of = db.relationship('WorkspaceMembers', backref = 'member_details')

    # Create a one-to-many relationship with Task model and put an invisible columns 'user_assigned_details' to the Task model and 'tasks'in the User Model accessible only via flask
    # Calling this attribute will return an array of all tasks a non-admin user have 
    task = db.relationship('Task', backref= 'user_assigned_details')
    # Create a one-to-many relationship with the TaskUpdate with sent_updates column in the User table and sender_details column on the TaskUpdate 
    sent_updates = db.relationship('TaskUpdates', backref='sender_details')
    

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

