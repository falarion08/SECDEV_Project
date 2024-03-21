from app.models import db
from datetime import datetime
from . import Workspace, User,TaskUpdates

class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    task_name = db.Column(db.String(80),nullable= False)
    workspace = db.Column(db.Integer, db.ForeignKey('workspace.workspace_id'))
    status = db.Column(db.String(20), nullable=False)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_user_email_address = db.Column(db.String(64), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    
    # Createa a one-to-many relationship with taskUpdates and create an invisible columns on tasks  as 'task_updates' 
    # and create an invisible column in task_updates as 'task_detials'
    task_updates = db.relationship('TaskUpdates', backref = 'task_details',cascade="all, delete")
    
    def __init__(self,task_name, assigned_user_email_address,due_date, owning_workspace, user_assigned_details):
        self.status = "To-Do"
        self.task_name = task_name
        self.assigned_user_email_address = assigned_user_email_address
        self.due_date = due_date
        self.owning_workspace = owning_workspace
        self.user_assigned_details = user_assigned_details

    