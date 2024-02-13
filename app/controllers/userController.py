from app.controllers import verify_password, hashPassword, verify_image, verify_email, verify_phone_number
from app.models.User import User,db

def create(user_email,password,phone_number,full_name,profile_picture):
    #verify_image(profile_picture)
    hashedResult = hashPassword(password)
    new_user = User(
        email=user_email,
        hash= hashedResult[1], 
        salt = hashedResult[0],
        full_name = full_name,
        phone_number=phone_number
    )       
    db.session.add(new_user)
    db.session.commit()

def check_email_valid(user_email):
    existing_user = User.query.filter_by(email=user_email).first()
    is_email_valid = verify_email(user_email)
    if existing_user or not is_email_valid:
        return False
    return True

def check_password_valid(password):
    is_password_valid = verify_password(password)
    if not is_password_valid:
        return False
    return True

def check_phone_number_valid(phone_number):
    is_phone_number_valid = verify_phone_number(phone_number)
    if not is_phone_number_valid:
        return False
    return True

def check_picture_valid(profile_picture):
    is_valid = verify_image(profile_picture)
    return is_valid