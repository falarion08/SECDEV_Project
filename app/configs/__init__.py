import os
from datetime import timedelta
from flask.logging import default_handler

def setup_configs(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345@127.0.0.1:5432/CSSECDEV"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Set to false to use less memory
    #app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['UPLOAD_FOLDER'] = os.getenv('FOLDER_UPLOAD')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_IMAGE_SIZE')) # 1MB Max
    app.config['RECAPTCHA_USE_SSL']= False
    app.config['RECAPTCHA_PUBLIC_KEY']= "6LcWx3MpAAAAAEM6Zce08cRhLriIcos5dI5YFpcE"
    app.config['RECAPTCHA_PRIVATE_KEY']="6LcWx3MpAAAAAPP_N_-NfwWhPeTPxyKHlM_60DTV"
    app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    #app.config['SECURITY_EMAIL_VALIDATOR_ARGS'] = {'check_deliverability': False}

