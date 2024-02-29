import re
import uuid as uuid
import bcrypt
import os


def verify_full_name(full_name):
    return re.match(r"^[A-Za-z -]+$", full_name)

def verify_email(user_email):
    return re.match(
        r"((?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))",
        user_email
        )

def verify_phone_number(phone_number):
    # FIXME: DO PHONE NUMBER REGEX HERE
    return re.match(r"\d{1,13}", phone_number)

def verify_password(user_password):
    """
        Password format:
        - Must contain characters between 12,64
        - Must contain at least one lowercase character
        - Must contain at least one uppercase character
        - Must contain at least one special character
        
        Return value: None or a matched string
    """
    return re.match(
        r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[`~!@#$%^&*()\-_=+\[\]\\|;:'\",<.>/?])[A-Za-z\d`~!@#$%^&*()\-_=+\[\]\\|;:'\",<.>/?]{12,64}$", 
        user_password
        )

def hashPassword(user_password):
    bytes = user_password.encode('utf-8')
    salt = bcrypt.gensalt()

    hash = bcrypt.hashpw(bytes,salt).decode('utf-8')
    salt = salt.decode('utf-8')

    return (salt,hash)

def verify_image(uploaded_image):
    ALLOWED_MIMETYPES = {"image/png", "image/jpeg", "image/jpg", "image/gif"}
    MAX_SIZE = int(os.getenv('MAX_IMAGE_SIZE'))
    print(MAX_SIZE)
    if not uploaded_image:
        return True

    if not uploaded_image.mimetype in ALLOWED_MIMETYPES:
        return False

    #print(len(cloned_image.read()))
    #if len(cloned_image.read()) > MAX_SIZE:
    #    return False
    return True
