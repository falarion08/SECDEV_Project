from flask import Flask
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
from app.models import db
from app.routes import register_blueprints
from app.configs import setup_db


from app.models.Files import Files

def create_app():
    # Allows you to load your .env file
    load_dotenv()

    # Create an instance of flask to run application
    app = Flask(__name__)
    csrf = CSRFProtect(app)

    # set app db configs
    setup_db(app)

    db.init_app(app)
    
    register_blueprints(app)

    # Create tables that does not exist in the database
    # app.app_context().push()
    # db.create_all()
    with app.app_context():
         db.create_all()

    return app
