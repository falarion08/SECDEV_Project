from flask import Flask
from app.models.user import db
from app.routes import register_blueprints
from dotenv import load_dotenv
import os

def create_app():
    # Allows you to load your .env file
    load_dotenv()

    # Create an instance of flask to run application
    app = Flask(__name__)

    # Connect to the database hosted online
    #DB_URL = os.environ.get("DATABASE_URL")
    #app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Set to false to use less memory
    #app.config['SQLALCHEMY_ECHO'] = True

    #db.init_app(app)

    register_blueprints(app)

    # Create tables that does not exist in the database
    app.app_context().push()
    #db.create_all()

    return app