from app.models import db

class Files(db.Model):
    __tablename__ = "files"
    
    file_id = db.Column(db.Integer,primary_key =True, unique =True,autoincrement=True)
    filename = db.Column(db.String(50), nullable = False)
    file_extension = db.Column(db.String(5), nullable = False)
    data = db.Column(db.LargeBinary, nullable = False)
    
    def __init__(self,filename,file_extension,data):
        self.filename = filename
        self.file_extension = file_extension
        self.data = data
    def json(self):
        
        return {'id': self.file_id, 'filename': self.filename, 'file_extension':self.file_extension, 'data':self.data}