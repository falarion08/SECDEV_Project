from flask import render_template, request, redirect, jsonify, url_for, make_response
from app.models.user import db, User
from . import main_bp

@main_bp.route('/', methods = ["GET", "POST"])
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

@main_bp.route('/register', methods = ["GET","POST"])
def registerPage():
    if request.method == "GET":
        return render_template('userRegisterPage.html')
    else:
        pass
