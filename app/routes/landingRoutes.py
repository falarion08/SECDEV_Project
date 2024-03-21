from flask import render_template, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from app.models.User import db, User
from app.controllers import userController
from app.utils.forms import RegistrationForm, LoginForm
from . import landing_bp, login_manager, limiter, admin_permission
import logging

# Initalize formatting for logging
logging.basicConfig(filename='sys.log', filemode='a', format='%(asctime)s  %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)

"""
    This python file is dedicated to the routes that are made available to unauthenticated users only.
"""

# Required decorator when using flask-login to find authenticated user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@landing_bp.route('/', methods=["GET", "POST"])
def home_page():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            if current_user.role == 'admin':
                return redirect(url_for('adminRoutes.admin_homepage'))
            else:
                return redirect(url_for('clientRoutes.client_homepage'))  
    return render_template('index.html')


@landing_bp.route('/login', methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login_page():
    
    form = LoginForm()
    
    # Checks to see if the user is logged in to prevent them from accessing the homepage
    if current_user.is_authenticated:
        session.permanent= True
        session.pop('_flashes', None)
        flash('You are already logged in!', 'error-msg')
        
        if current_user.role == 'admin':
            return redirect(url_for('adminRoutes.admin_homepage'))
        else:
           return redirect(url_for('clientRoutes.client_homepage'))  
    
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        
        if not user:
            session.pop('_flashes', None)
            flash("Email address or password incorrect", 'error-msg')
            return redirect(url_for('landingRoutes.login_page'))
            
        if userController.check_password_hash(user.hash, form.password.data):
            login_user(user)
            flash("Login successful", "success-msg")
            
            logging.info(f'[{user.email} - {user.role}] has logged in')

            if current_user.role == 'admin':
                return redirect(url_for('adminRoutes.admin_homepage'))
            else:
                return redirect(url_for('clientRoutes.client_homepage'))
        else:
            session.pop('_flashes', None)
            flash("Email address or password incorrect", 'error-msg')
            return redirect(url_for('landingRoutes.login_page'))
            
            
    return render_template('userLogin.html', form=form)


@landing_bp.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    user_email = current_user.email
    user_role = current_user.role
    logout_user()
    session.pop('_flashes', None)
    flash("You have been logged out.", "success-msg")
    logging.info(f'[{user_email} - {user_role}] has logged out')
    return redirect(url_for('landingRoutes.login_page'))

@landing_bp.route('/register', methods = ["GET","POST"])
@limiter.limit("5 per minute", methods=["POST"])
def register_page():
    
    form = RegistrationForm()
    if current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You are already logged in!', 'error-msg')
        if current_user.role == 'admin':
            return redirect(url_for('adminRoutes.admin_homepage'))
        else:
            return redirect(url_for('clientRoutes.client_homepage'))
    
    if form.validate_on_submit():
        validation_msg = userController.validate_registration(
            form.email.data,
            form.password.data,
            form.confirm_password.data,
            form.phone_number.data,
            form.profile_picture.data,
            form.full_name.data
        )
        if validation_msg is not None:
            flash(validation_msg, 'error-msg')
            return redirect(url_for('landingRoutes.register_page'))

        userController.create(
            user_email=form.email.data,
            password=form.password.data,
            full_name=form.full_name.data,
            phone_number=form.phone_number.data,
            profile_picture=form.profile_picture.data
        )
        logging.info(f'User with email {form.email.data} has registered')
        flash('Registration successful', 'success-msg')
        return redirect(url_for('landingRoutes.login_page'))

    return render_template('userRegisterPage.html', form=form)

