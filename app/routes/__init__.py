# This can remain empty unless you need to initialize something
from flask import Blueprint

main_bp = Blueprint('main', __name__)
# admin_bp = Blueprint('admin', __name__)

from . import main

def register_blueprints(app):
    app.register_blueprint(main_bp)
    # app.register_blueprint(admin_bp)