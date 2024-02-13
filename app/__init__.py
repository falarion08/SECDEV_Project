import os
from flask import Flask
from app.models import db
from app.routes import register_blueprints
from app.configs import setup_db
from dotenv import load_dotenv

from app.models.Files import Files

def create_app():
    # Allows you to load your .env file
    load_dotenv()

    # Create an instance of flask to run application
    app = Flask(__name__)

    # Connect to the database hosted online
    DB_URL = os.getenv("DATABASE_URL")
    upload_folder = os.getenv("FOLDER_UPLOAD")

    # set app db configs
    setup_db(app, DB_URL,upload_folder)

    db.init_app(app)
    
    register_blueprints(app)

    # Create tables that does not exist in the database
    app.app_context().push()
    db.create_all()

    return app
