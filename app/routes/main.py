from flask import abort, render_template, request, redirect, jsonify, url_for, make_response
from app.models.user import db, User
from . import main_bp, errors
from app.controllers import userController


@main_bp.route('/', methods = ["GET", "POST"])
def homepage():
    # try:
    #     new_user = User(username='LAMOS', email='lalamove@gmail.com')
    #     db.session.add(new_user)
    #     db.session.commit()
    # except Exception as e:
    #     print(e)
    if request.method == "GET":
        return render_template('index.html')
    else:
        pass

@main_bp.route('/login', methods = ["GET", "POST"])
def loginPage():
    if request.method == "GET":
        return render_template('userLogin.html')
    else:
        pass

@main_bp.route('/register', methods = ["GET","POST"])
def registerPage():
    if request.method == "GET":
        return render_template('userRegisterPage.html')
    else:
        userController.create(
            user_email=request.form['userEmail'],
            password=request.form['password'],
            full_name=request.form['userFullName'],
            phone_number=request.form['phone_number']
        )
        return redirect('/register')

@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template(
        'errorPage.html',
        error_num=404,
        error_text="Page Not Found"), 404

@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_template(
        'errorPage.html',
        error_num=500,
        error_text="Internal Server Error"), 500