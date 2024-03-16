from . import db,User

class Workspace(db.Model):
    __tablename__ = 'workspace'
    workspace_id = db.Column(db.Integer, primary_key = True, autoincrement = True,unique=True)
    workspace_name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        
    def __init__(self, workspace_name,owner):
        self.workspace_name = workspace_name
        self.owner = owner
    
    def json(self):
        return {
            'workspace_id': self.workspace_id,
            'workspace_name': self.workspace_name,
            'owner_id': self.owner_id
        }