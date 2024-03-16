from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_principal import Principal
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.models import db
from app.routes import register_blueprints, setup_login, limiter
from app.configs import setup_configs
from app.controllers.userController import create_admin

# Used to create the models that is defined
from app.models import exportModels

def create_app():
    # Allows you to load your .env file
    load_dotenv()
    
    # Create an instance of flask to run application
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    migrate = Migrate()
    # talisman = Talisman(app)  
    principals = Principal(app)

    # set app db configs
    setup_configs(app)
    # setup_talisman(talisman)
    setup_login(app)
    db.init_app(app)
    
    migrate.init_app(app, db)
    limiter.init_app(app)
    register_blueprints(app)

    # Create tables that does not exist in the database and fill the database with a given seed if any.
    app.app_context().push()
    db.create_all()
    create_admin()

    return app
