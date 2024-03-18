from flask import render_template, flash, redirect, url_for, session,request
from flask_login import login_user, login_required, logout_user, current_user
from app.models.User import db, User
from . import admin_bp,login_manager
from app.models.Workspace import Workspace
from app.models.WorkspaceMembers import WorkspaceMembers
from  wtforms import Label
import app.utils.forms as form

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
    
    _delete_form = form.deleteForm()
    
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
    
    _form = form.createWorkspace() 
    
    if _form.validate_on_submit():
        workspace = Workspace(_form.workspace_name.data, current_user)
        db.session.add(workspace)
        db.session.commit()
        
        return redirect(url_for('adminRoutes.admin_homepage'))
    
    return render_template('createWorkspace.html', form = _form)

@admin_bp.post('/delete/<int:workspace_id>')
@login_required
def delete_workspace(workspace_id):

    if form.deleteForm(request.form).validate_on_submit():
        workspace = Workspace.query.get(int(workspace_id))
        db.session.delete(workspace)
        db.session.commit()
        
    return redirect(url_for('adminRoutes.admin_homepage'))

@admin_bp.route('/edit_workspace/<int:workspace_id>', methods = ["GET","POST"])
@login_required
def edit_workspace(workspace_id):
    
    # Query all current members of the workspace given an 
    current_workspace_members = WorkspaceMembers.query.filter(workspace_id = workspace_id).all()
    
    # All forms for this page are instantiated here
    _updateNameForm = form.createWorkspace()
    _new_member_form = form.addMemberWorkspaceForm()
    
    remove_member = form.deleteForm()
    remove_member.submit.label = Label(remove_member.submit.id, 'Remove member')

    # Validate if the user tries to modify the workspace name
    if _updateNameForm.validate_on_submit():
        workspace = Workspace.query.get(int(workspace_id))
        workspace.workspace_name = _updateNameForm.workspace_name.data
        db.session.commit()

    return render_template('editWorkspace',workspace_id = workspace_id, updateWorkspaceNameForm = _updateNameForm, new_member_form = _new_member_form, 
                           workspace_members = current_workspace_members)
    
@admin_bp.post('/edit_workspace/add_member/<int:workspace_id>')
@login_required
def add_member(workspace_id):
    
    add_member_form = form.addMemberWorkspaceForm(request.form)
    
    # Validate if the user tries to add a new member to the workspace  
    if add_member_form.validate_on_submit():
        
        # Get the new user that the admin is trying to add
        user = User.query.filter(email = add_member_form.email_address.data).first()

        # If the query returns a result save the the member to the workspace_members table
        if user: 
            workspace = Workspace.query.get(int(workspace_id))
            new_member = WorkspaceMembers(workspace, user)
            
            db.session.add(new_member)
            db.session.commit()

@admin_bp.post('/edit_workspace/remove_member/<int:member_id>')
@login_required
def remove_member(member_id):
    
    if form.deleteForm(request.form).validate_on_submit():
        member = User.query.get(int(member_id))
        db.session.delete(member)
        db.session.commit()
    
    return redirect(url_for('adminRoutes.edit_workspace'))
    


        
    
    