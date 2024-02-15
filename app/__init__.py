from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from app.models import db
from app.routes import register_blueprints, setup_login,limiter
from app.configs import setup_db
from app.controllers.userController import create_admin

def create_app():
    # Allows you to load your .env file
    load_dotenv()

    # Create an instance of flask to run application
    app = Flask(__name__)
    csrf = CSRFProtect()

    csrf.init_app(app)

    setup_login(app)

    # set app db configs
    setup_db(app)
    
    limiter.init_app(app)

    db.init_app(app)
    
    register_blueprints(app)

    # Create tables that does not exist in the database
    with app.app_context():
        db.create_all()
        create_admin()


    return app
