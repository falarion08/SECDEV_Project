import re
import bcrypt

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
