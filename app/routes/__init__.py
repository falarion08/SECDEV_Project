# This can remain empty unless you need to initialize something
from flask import Blueprint
from flask_login import LoginManager
import bcrypt  

# Allows the action of logging in and logging out users
login_manager = LoginManager()


#  Creating blueprints for routes
main_bp = Blueprint('main', __name__)
errors = Blueprint('errors', __name__)
defaultUser_bp = Blueprint('defaultUser', __name__)
# admin_bp = Blueprint('admin', __name__)

def checkPassword(userPassword, hash):
    userBytes = userPassword.encode('utf-8')
    return bcrypt.checkpw(userBytes,hash)
    


# do not remove this, it will cause all routes to result in 404 error
from . import main

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(errors)
    app.register_blueprint(defaultUser_bp)
    # app.register_blueprint(admin_bp)
    
