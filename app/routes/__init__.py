# This can remain empty unless you need to initialize something
from flask import Blueprint
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_principal import Permission, RoleNeed


"""
    This python file is dedicated to initializing routes, authentication, and request limiter using the 
    following following libraries:
    - flask-blueprint
    - flask-login
    - flask-limitier
"""

# Creating routes
landing_bp = Blueprint('landingRoutes', __name__)
admin_bp = Blueprint('adminRoutes', __name__)
client_bp = Blueprint('clientRoutes', __name__)
error_bp = Blueprint('errorRoutes', __name__)


# Creating login-manager
login_manager = LoginManager()

# Specificying the role need for admin routes is "admin"
admin_permission = Permission(RoleNeed('admin'))


# Initialzing how many limit request a user can make
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Import route files to prevent 404 error on every url
from . import landingRoutes,adminRoutes,clientRoutes,errorRoutes

# Configuring flask-login
def setup_login(app):
    login_manager.init_app(app)
    login_manager.login_view = 'landingRoutes.login_page'
    login_manager.session_protection = 'strong'

# Registering routes to the flask application
def register_blueprints(app):
    
    # Adding middleware functions to blueprints
    # app.before_request_funcs = {
    #     'adminRoutes':[],
    #     'clientRoutes':[]
    # }
    
    app.register_blueprint(landing_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(admin_bp, url_prefix ='/admin', template_folder = 'template',static_folder = 'static')
    app.register_blueprint(client_bp, url_prefix= '/client',template_folder = 'template',static_folder = 'static')
