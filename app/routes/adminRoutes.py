from flask import render_template, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from app.models.User import db, User
from . import admin_bp,login_manager
from app.utils.forms import createWorkspace,deleteForm
from app.models.Workspace import Workspace
from  wtforms import Label

# Required decorator when using flask-login to find authenticated user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@admin_bp.route('/', methods=["GET", "POST"])
@login_required
def admin_homepage():
    curr_role = current_user.role
    
    if curr_role != 'admin':
        
        session.pop('_flashes', None)
        flash('You must be the admin to access the admin page!', 'error-msg')
        
        return redirect(url_for('landingRoutes.login_page'))
    
    users = User.query.filter(User.role != 'admin').all()
    
    _delete_form = deleteForm()
    
    # Dynamically change the message of the submit button
    _delete_form.submit.label = Label(_delete_form.submit.id, 'Delete Workspace')
    
    return render_template('dashboard.html', user_fullName = current_user.full_name, workspaces = current_user.workspaces,
                           delete_form = _delete_form)

@admin_bp.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash("You have been logged out.", "success-msg")
    
    return redirect(url_for('landingRoutes.login_page'))

@admin_bp.route("/create_workspace", methods =["GET","POST"])
@login_required
def create_workspace():
    
    form = createWorkspace()
    
    if form.validate_on_submit():
        workspace = Workspace(form.workspace_name.data, current_user)
        db.session.add(workspace)
        db.session.commit()
        
        return redirect(url_for('adminRoutes.admin_homepage'))
        
    
    
    return render_template('createWorkspace.html', form = form)

@admin_bp.post('/delete/<int:workspace_id>')
@login_required
def delete_workspace(workspace_id):
    workspace = Workspace.query.get(int(workspace_id))
    db.session.delete(workspace)
    db.session.commit()
    
    return redirect(url_for('adminRoutes.admin_homepage'))