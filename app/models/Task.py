from app.models import db
from datetime import datetime
from . import Workspace, User

class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)

    workspace = db.Column(db.Integer, db.ForeignKey('workspace.workspace_id'))

    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigner_user_email_address = db.Column(db.String(64), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    
    
    def __init__(self, assigned_user_email_address,due_date, owning_worksapce, user_assigned_details):
        self.assigned_user_id = assigned_user_email_address
        self.due_date = due_date
        self.owning_workspace = owning_worksapce
        self.user_assigned_details = user_assigned_details

    