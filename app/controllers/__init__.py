import re
import bcrypt
from werkzeug.utils import secure_filename
import os
from PIL import Image

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
        r'\A(?=.*?[a-z]+)(?=.*?[A-Z]+)(?=.*?\d+)(?=.*\W+)[^s]{12,64}$', 
        user_password
        )

def hashPassword(user_password):
    bytes = user_password.encode('utf-8')
    salt = bcrypt.gensalt()

    hash = bcrypt.hashpw(bytes,salt)

    return (salt,hash)


def verify_image(uploaded_image):
    ALLOWED_EXTENSIONS = {"png", "jpeg", "jpg"}    
    FOLDER_UPLOAD = os.environ.get("FOLDER_UPLOAD")
    if uploaded_image.filename != '':

        filename = secure_filename(uploaded_image.filename).lower()
        uploaded_image.save(os.path.join(FOLDER_UPLOAD,filename))  
        
        try:
            img = Image.open(FOLDER_UPLOAD + filename)            
        
            if img.format.lower() in  ALLOWED_EXTENSIONS:
                return True
            else:
                False
        
        except:
            print("File is not an image")
            return False
        

