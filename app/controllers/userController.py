import os
import bcrypt
import uuid
from werkzeug.utils import secure_filename
from app.controllers import verify_password, hashPassword, verify_image, verify_email, verify_phone_number
from app.models.User import User,db

def create(user_email,password,phone_number,full_name,profile_picture):
        profile_picture_file_name = upload_file(profile_picture)  
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

def create_admin():
    admin_user = User.query.filter_by(role="admin").first()

    if admin_user:
        return
    password = hashPassword('asdfQWERTY1357!')
    admin_user = User(
        email='admin@admin.com',
        hash= password[1],
        salt = password[0],
        full_name = "Admin Account",
        phone_number='123456789012',
        profile_picture=None,
        role="admin"
    )
    db.session.add(admin_user)
    db.session.commit()

def validate_registration(user_email, password, confirm_password, phone_number, profile_picture):
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
    return None

def check_password_hash(hashed_password, password):
    user_bytes = password.encode('utf-8')
    hashed_pw = hashed_password.encode('utf-8')
    return bcrypt.checkpw(user_bytes, hashed_pw)

def upload_file(uploaded_image):
    if not uploaded_image:
        return None
    FOLDER_UPLOAD = os.environ.get('FOLDER_UPLOAD')
    picture_filename = secure_filename(uploaded_image.filename)
    new_filename = str(uuid.uuid1()) + '_' + picture_filename
    uploaded_image.save(os.path.join(FOLDER_UPLOAD, new_filename))
    return new_filename