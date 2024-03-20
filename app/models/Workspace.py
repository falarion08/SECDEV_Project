from . import db
from . import Task

class Workspace(db.Model):
    __tablename__ = 'workspace'
    workspace_id = db.Column(db.Integer, primary_key = True, autoincrement = True,unique=True)
    workspace_name = db.Column(db.String(100), nullable=False)
    
    # Reference id in Users model as foreign key
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Create a one-to-many relationship with WorkspaceMembers model and put an invisible columns 'workspace' to the WorkspaceMembers model and 'members' to the Workspace Model accessible only via flask
    # Calling this attribute will return an array of all membes of the workspace
    members = db.relationship('WorkspaceMembers', backref='workspace')
    
    
    # Create a one-to-many relationship with Task model and put an invisible columns 'owning_workspace' to the Task model and 'tasks' to the Workspace Model accessible only via flask
    # Calling this attribute will return an array of all membes of the workspace
    tasks = db.relationship('Task', backref='owning_workspace')

        
    def __init__(self, workspace_name,owner):
        """
        DataTypes
            workspace_name : String
            owner: User 
        """
        self.workspace_name = workspace_name
        self.owner = owner
    
    def json(self):
        return {
            'workspace_id': self.workspace_id,
            'workspace_name': self.workspace_name,
            'owner_id': self.owner_id
        }