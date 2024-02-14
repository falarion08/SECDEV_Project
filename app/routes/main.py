from flask import render_template, request, flash, redirect, jsonify, url_for, make_response
import flask_login
from flask_login import login_user, logout_user,current_user
from app.models import db
from app.models.User import User
from app.controllers import userController
from app.utils.forms import RegistrationForm, LoginForm
from . import main_bp, errors,login_manager,checkPassword

# Creates a user loader callback that returns the user object given an email
@login_manager.user_loader
def load_user(user_email):
    return User.query.filter_by(email=user_email)

@main_bp.route('/', methods = ["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        print(form.email.data, form.password.data)
        # TODO: DO LOGIN STUFF (auth)?
        
        # Check if the user is in the database
        existing_user = User.query.filter_by(email = form.email.data).first()
        
        if existing_user and checkPassword(form.password.data,existing_user['hash']):
            # Authenticate user
            login_user(existing_user)
            return redirect('/default')
    return render_template('userLogin.html', form=form)

@main_bp.route('/register', methods = ["GET","POST"])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.email.data, form.password.data, form.full_name.data, form.phone_number.data)
        validation_msg = userController.validate_registration(
            form.email.data,
            form.password.data,
            form.confirm_password.data,
            form.phone_number.data,
            form.full_name.data
        )
        if validation_msg is not None:
            flash(validation_msg, 'error-msg')
            return redirect('/register')
        userController.create(
            user_email=form.email.data,
            password=form.password.data,
            full_name=form.full_name.data,
            phone_number=form.phone_number.data,
            profile_picture=form.profile_picture.data
        )
        flash('Registration successful', 'success-msg')
        return redirect('/login')
    return render_template('userRegisterPage.html', form=form)

@errors.app_errorhandler(404)
def error_404(e):
    return render_template(
        'errorPage.html',
        error_num=404,
        error_text="Page Not Found"), 404

@errors.app_errorhandler(500)
def error_500(e):
    return render_template(
        'errorPage.html',
        error_num=500,
        error_text="Internal Server Error"), 500
