from app.models.Files import Files,db

def uploadFile(upload_file):
    file_format = upload_file.filename.split('.')
    file_format[1] = file_format[1].lower()
    
    file = Files(filename=upload_file.filename,file_extension=file_format[1],
                 data= upload_file.read())
    
    db.session.add(file)
    db.session.commit()
    
    return file.file_id