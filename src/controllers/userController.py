import os
import bcrypt
import uuid
from werkzeug.utils import secure_filename
from src.controllers import verify_password, hashPassword, verify_image, verify_email, verify_phone_number, verify_full_name
from src.models.User import User,db
from src.models.TaskFiles import TaskFiles, db
import fleep

def create(user_email,password,phone_number,full_name,profile_picture):
        profile_picture_file_name = upload_file(profile_picture, 'profile_picture')  
        hashedResult = hashPassword(password)
        new_user = User(
            email=user_email,
            hash= hashedResult[1], 
            salt = hashedResult[0],
            full_name = full_name,
            phone_number=phone_number,
            profile_picture=profile_picture_file_name,
            role="user"
        )
        db.session.add(new_user)
        db.session.commit()


def validate_registration(user_email, password, confirm_password, phone_number, profile_picture, full_name):
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
    # Check if uploaded image is valid
    is_picture_valid = verify_image(profile_picture)
    if not is_picture_valid:
        return 'Profile picture is invalid'
    is_full_name_valid = verify_full_name(full_name)
    if not is_full_name_valid:
        return 'Full name is invalid.'

    return None

def check_password_hash(hashed_password, password):
    user_bytes = password.encode('utf-8')
    hashed_pw = hashed_password.encode('utf-8')
    return bcrypt.checkpw(user_bytes, hashed_pw)

def upload_file(file, mode):
    if not file:
        return None
    
    FOLDER_UPLOAD = os.environ.get('FOLDER_UPLOAD')
    filename = secure_filename(file.filename)
    new_filename = str(uuid.uuid1()) + '_' + filename
    file.save(os.path.join(FOLDER_UPLOAD, new_filename))

    with open(os.path.join(FOLDER_UPLOAD, new_filename), "rb") as _file:
        info = fleep.get(_file.read(128))

    if mode == 'profile_picture':
        if info.type_matches('raster-image'):
            if info.extension_matches('jpg') and info.mime_matches('image/jpeg'):
                return new_filename
            if info.extension_matches('gif') and info.mime_matches('image/gif'):
                return new_filename
            if info.extension_matches('png') and info.mime_matches('image/png'):
                return new_filename
    elif mode == 'file':
        if info.type_matches('document') and info.extension_matches('pdf') and info.mime_matches('application/pdf'):
            return new_filename
    os.remove(os.path.join(FOLDER_UPLOAD, new_filename))
    return None