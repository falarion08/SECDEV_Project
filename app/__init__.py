from flask import Flask
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
from app.models import db
from app.routes import register_blueprints,login_manager
from app.configs import setup_db



def create_app():
    # Allows you to load your .env file
    load_dotenv()

    # Create an instance of flask to run application
    app = Flask(__name__)
<<<<<<< Updated upstream
    csrf = CSRFProtect(app)

=======
    
    # Allows the action to log-in and log-out users
    login_manager.init_app(app)
    
    csrf = CSRFProtect()
    csrf.init_app(app)
    
>>>>>>> Stashed changes
    # set app db configs
    setup_db(app)
    db.init_app(app)
    
    # Register routes to the application
    register_blueprints(app)

    # Create tables that does not exist in the database
    app.app_context().push()
    db.create_all()


    return app
