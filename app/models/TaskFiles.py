from . import db, User, Task


class TaskFiles(db.Model):
    __tablename__ = 'task_files'
    
    file_id = db.Column(db.Integer, primary_key = True, autoincrement= True, unique = True)
    file = db.Column(db.String(), nullable= True)

    # Reference the table users and set the foreign key value as user_id
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Reference the table tasks and set the foreignKey as task_id 
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'))

    def __init__(self, file, uploader_details, task_details):
        """
            DataTypes:
            file = String
        """
        self.file = file
        self.uploader_details = uploader_details
        self.task_details = task_details
        
