from flask import render_template, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from app.models.User import db, User
from . import admin_bp,login_manager

# Required decorator when using flask-login to find authenticated user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@admin_bp.route('/', methods=["GET", "POST"])
@login_required
def admin_homepage():
    print("helloooo")
    curr_role = current_user.role
    
    if curr_role != 'admin':
        
        session.pop('_flashes', None)
        flash('You must be the admin to access the admin page!', 'error-msg')
        
        return redirect(url_for('landingRoutes.login_page'))
    
    users = User.query.filter(User.role != 'admin').all()
    
    return render_template('admin.html', users=users)

@admin_bp.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash("You have been logged out.", "success-msg")
    
    return redirect(url_for('main.login_page'))
