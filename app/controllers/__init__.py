import re
import bcrypt
from werkzeug.utils import secure_filename
import os
from PIL import Image


def verify_email(user_email):
    return re.match(
        r"((?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))",
        user_email
        )

def verify_phone_number(phone_number):
    # FIXME: DO PHONE NUMBER REGEX HERE
    return re.match(r"\d{10,20}", phone_number)

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

    hash = bcrypt.hashpw(bytes,salt)

    return (salt,hash)


def verify_image(uploaded_image):
    ALLOWED_EXTENSIONS = {"png", "jpeg", "jpg", "gif"}
    FOLDER_UPLOAD = os.environ.get("FOLDER_UPLOAD")
    #PLACEHOLDER = "../static/images/PLACEHOLDER.jpg"

    # #TODO: if user doesn't upload an image, use a placeholder image
    # if not uploaded_image:
    #     return 
    
    if uploaded_image.filename != '':
        filename = secure_filename(uploaded_image.filename).lower()
        uploaded_image.save(os.path.join(FOLDER_UPLOAD,filename)) #FIXME: FileNotFoundError No such file or directory occurs when a file is uploaded
        
        try:
            img = Image.open(FOLDER_UPLOAD + filename)            
        
            if img.format.lower() in ALLOWED_EXTENSIONS:
                return True
            else:
                False
        
        except:
            print("File is not an image")
            return False
        

