from app.controllers import verify_password, hashPassword, verify_image, verify_email, verify_phone_number, verify_image_test
from app.models.User import User,db
from app.controllers.fileController import uploadFile 
import os
import bcrypt

def create(user_email,password,phone_number,full_name,profile_picture):
        profilePictureId = verify_image_test(profile_picture)
        #profilePictureId = uploadFile(profile_picture)   
        hashedResult = hashPassword(password)
        new_user = User(
            email=user_email,
            hash= hashedResult[1], 
            salt = hashedResult[0],
            full_name = full_name,
            phone_number=phone_number,
            profile_picture_id=profilePictureId
        )
        db.session.add(new_user)
        db.session.commit()
        #os.remove(os.environ.get("FOLDER_UPLOAD")+profile_picture.filename)


# : Add profile picture validation
def validate_registration(user_email, password, confirm_password, phone_number, full_name):
    # Check email validity
    existing_user = User.query.filter_by(email=user_email).first()
    is_email_valid = verify_email(user_email)
    if existing_user:
        return 'Email address is already in use.'
    if not is_email_valid:
        return 'Email address is invalid.'
    # Check password validity
    is_password_valid = verify_password(password)
    if not is_password_valid:
        return 'Password is invalid.'
    # Check phone number validity
    is_phone_number_valid = verify_phone_number(phone_number)
    if not is_phone_number_valid:
        return 'Phone number is invalid.'
    # Check if password matches
    if password != confirm_password:
        return 'Passwords did not match.'
    return None

def check_password_hash(hashed_password, password):
    user_bytes = password.encode('utf-8')
    hashed_pw = hashed_password.encode('utf-8')
    return bcrypt.checkpw(user_bytes, hashed_pw)