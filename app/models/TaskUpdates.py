from . import db, User, Task
from sqlalchemy.sql import func
class TaskUpdates(db.Model):
    __tablename__ = 'task_updates'
    
    task_update_id = db.Column(db.Integer, primary_key = True, autoincrement= True, unique = True)
    message = db.Column(db.String(256), nullable= False)
    date_time_sent = db.Column(db.DateTime,nullable=False, server_defeault = func.now())

    # Reference the table users and set the foreign key value as user_id
    sent_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Reference the table tasks and set the foreignKey as task_id 
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'))

    def __init__(self, message, sent_by_user,task_details):
        """
            DataTypes:
            message = String
            sent_by_user = User
            task_details = Task
        """
        self.message = message
        self.sent_by_user = sent_by_user
        self.task_details = task_details
        
        


