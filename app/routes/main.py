from flask import render_template, request, flash, redirect, jsonify, url_for, make_response, session
from flask_login import login_user, login_required, logout_user, current_user
from app.models.User import db, User
from app.controllers import userController
from app.utils.forms import RegistrationForm, LoginForm
from . import admin_bp, main_bp, errors, login_manager, limiter, admin_permission


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@admin_bp.route('/admin/delete/<int:id>')
@login_required
def delete_user(id):
    curr_role = current_user.role
    if curr_role != 'admin':
        session.pop('_flashes', None)
        flash('You must be the admin to perform this action!', 'error-msg')
        return redirect(url_for('main.dashboard_page'))
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        session.pop('_flashes', None)
        flash('User was successfully deleted!', 'success-msg')
        return redirect(url_for('admin.admin_page'))
    except Exception as e:
        print(e)
        flash('Oops! There was an error deleting the user.', 'error-msg')
        return redirect(url_for('admin.admin_page'))


@admin_bp.route('/admin', methods=["GET", "POST"])
@login_required
def admin_page():
    curr_role = current_user.role
    if curr_role != 'admin':
        session.pop('_flashes', None)
        flash('You must be the admin to access the admin page!', 'error-msg')
        return redirect(url_for('main.dashboard_page'))
    users = User.query.filter(User.role != 'admin').all()
    return render_template('admin.html', users=users)

@main_bp.route('/', methods=["GET", "POST"])
def home_page():
    users = User.query.count()
    return render_template('index.html', users=users)

@main_bp.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard_page():
    return render_template('dashboard.html')


@main_bp.route('/login', methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login_page():
    form = LoginForm()
    if current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You are already logged in!', 'error-msg')
        return redirect(url_for('main.dashboard_page'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if userController.check_password_hash(user.hash, form.password.data):
                login_user(user)
                flash("Login successful", "success-msg")
                return redirect(url_for('main.dashboard_page'))
            else:
                flash("Login failed", 'error-msg')
        else:
            flash("User not found", 'error-msg')
    return render_template('userLogin.html', form=form)

@main_bp.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash("You have been logged out.", "success-msg")
    return redirect(url_for('main.login_page'))

@main_bp.route('/register', methods = ["GET","POST"])
@limiter.limit("5 per minute", methods=["POST"])
def register_page():
    form = RegistrationForm()
    if current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You are already logged in!', 'error-msg')
        return redirect(url_for('main.dashboard_page'))
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
            return redirect(url_for('main.register_page'))

        userController.create(
            user_email=form.email.data,
            password=form.password.data,
            full_name=form.full_name.data,
            phone_number=form.phone_number.data,
            profile_picture=form.profile_picture.data
        )
        flash('Registration successful', 'success-msg')
        return redirect(url_for('main.login_page'))

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

@errors.app_errorhandler(413)
def error_413(e):
    return render_template(
        'errorPage.html',
        error_num=413,
        error_text="Request Entity Too Large"), 413

@errors.app_errorhandler(429)
def error_429(e):
    return render_template(
        'errorPage.html',
        error_num=429,
        error_text="Too Many Requests"), 429
    
