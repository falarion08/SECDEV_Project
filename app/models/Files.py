from app.models import db

class Files(db.Model):
    __tablename__ = "files"
    
    id = db.Column(db.Integer,primary_key =True,nullable=False, unique =True)
    filename = db.Column(db.String(50), nullable = False)
    file_extension = db.Column(db.String(5), nullable = False)
    data = db.Column(db.LargeBinary, nullable = False)
    
    def __init__(self,id,filename,file_extension,data):
        self.id = id
        self.filename = filename
        self.file_extension = file_extension
        self.data = data
    def json(self):
        
        return {'id': self.id, 'filename': self.filename, 'file_extension':self.file_extension, 'data':self.data}