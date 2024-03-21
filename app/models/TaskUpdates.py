from . import db, User, Task
from sqlalchemy.sql import func
from datetime import datetime
class TaskUpdates(db.Model):
    __tablename__ = 'task_updates'
    
    task_update_id = db.Column(db.Integer, primary_key = True, autoincrement= True, unique = True)
    message = db.Column(db.String(256), nullable= False)
    date_time_sent = db.Column(db.DateTime,nullable=False, server_default=func.now())
    edited = db.Column(db.Boolean, default=False, nullable=True)

    # Reference the table users and set the foreign key value as user_id
    sent_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Reference the table tasks and set the foreignKey as task_id 
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'))

    def __init__(self, message, sender_details, task_details, edited):
        """
            DataTypes:
            message = String
            sender_details = User
            task_details = Task
            edited = Boolean
        """
        self.message = message
        self.date_time_sent = datetime.utcnow()
        self.sender_details = sender_details
        self.task_details = task_details
        self.edited = edited
        
        


