from . import db

class WorkspaceMembers(db.Model):
    __tablename__ = 'workspace_members'
    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    
    # Reference the workspace_id column of the Workspace model as a foreign key
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.workspace_id'),nullable = False)

    # Reference the id column of the User model as a foreign key
    member_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    
    def __init__(self,workspace,user):
        """
        DataTypes:
            workspace: Workspace 
            user = User
        """
        self.workspace = workspace
        self.member_details = user
        
    def json(self):
        return {
            'id':self.id,
            'workspace_id':self.workspace_id,
            'member_id': self.member_id,
        }