from app.controllers import verify_password,hashPassword,verify_image
from app.models.User import User,db
from app.controllers.fileController import uploadFile 
import os

def create(user_email,password,phone_number,full_name,profile_picture):
    isPasswordValid = verify_password(password)
    
    if isPasswordValid:
        userList = User.query.filter_by(email= user_email).first()
        print('hey')

        if(userList is None):
            if verify_image(profile_picture):
                
                profilePictureId = uploadFile(profile_picture)
                
                hashedResult = hashPassword(password)
                new_user = User(email=user_email,hash= hashedResult[1], salt = hashedResult[0],
                                full_name = full_name,phone_number=phone_number,profile_picture_id=profilePictureId)       
                
                db.session.add(new_user)
                db.session.commit()
                
                os.remove(os.environ.get("FOLDER_UPLOAD")+profile_picture.filename)
            else:
                print('Image uploaded does not meet required file extenisons')
        else:
            print('User record already exist')
    else:
        print('Password not valid')

