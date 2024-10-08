import os
from datetime import timedelta
from flask.logging import default_handler

def setup_configs(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Set to false to use less memory
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = os.getenv('FOLDER_UPLOAD')
    app.config['MAX_CONTENT_LENGTH'] =int(os.getenv("MAX_FILE_UPLOAD_SIZE")) # 5MB Max
    app.config['RECAPTCHA_USE_SSL']= False
    app.config['RECAPTCHA_PUBLIC_KEY']= os.getenv("RECAPTCHA_PUBLIC_KEY")
    app.config['RECAPTCHA_PRIVATE_KEY']=os.getenv("RECAPTCHA_PRIVATE_KEY")
    app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    #app.config['SECURITY_EMAIL_VALIDATOR_ARGS'] = {'check_deliverability': False}

