from flask import Flask,render_template, request,redirect,jsonify, make_response
from dotenv import load_dotenv
import os 
from Contoller.database import db
from Contoller.models import User

# Allows you to load your .env file
load_dotenv()

# Create an instance of flask to run application
app = Flask(__name__)

# Connect to the database hosted online
DB_URL = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Set to false to use less memory
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

# Create tables that does not exist in the database
app.app_context().push()
db.create_all()
 

@app.route('/', methods = ["GET", "POST"])
def homepage():
    # try:
    #     new_user = User(username='LAMOS', email='lalamove@gmail.com')
    #     db.session.add(new_user)
    #     db.session.commit()
    # except Exception as e:
    #     print(e)
    if request.method == "GET":
        return render_template('userLogin.html')
    else:
        pass

@app.route('/register', methods = ["GET","POST"])
def registerPage():
    if request.method == "GET":
        return render_template('userRegisterPage.html')
    else:
        pass
    


if __name__ == '__main__':
    app.run(debug=True)
    
    
