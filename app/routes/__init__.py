# This can remain empty unless you need to initialize something
from flask import Blueprint
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

main_bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__)
errors = Blueprint('errors', __name__)
login_manager = LoginManager()

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# do not remove this, it will cause all routes to result in 404 error
from . import main

def setup_login(app):
    login_manager.init_app(app)
    login_manager.login_view = 'main.login_page'

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(errors)
    app.register_blueprint(admin_bp)
    
