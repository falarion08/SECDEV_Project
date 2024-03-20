from flask import render_template, flash, redirect, url_for, session,request
from flask_login import login_required, current_user
from app.models.User import db, User
from . import admin_bp,login_manager
from app.models.Task import Task
from app.models.Workspace import Workspace
from app.models.WorkspaceMembers import WorkspaceMembers
from  wtforms import Label
import app.utils.forms as form


# Required decorator when using flask-login to find authenticated user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@admin_bp.route('/admin', methods=["GET", "POST"])
@login_required
def admin_homepage():
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        return redirect(url_for('clientRoutes.client_homepage'))
    
    users = User.query.filter(User.role != 'admin').all()
    
    _delete_form = form.deleteForm()
    
    # Dynamically change the message of the submit button
    _delete_form.submit.label = Label(_delete_form.submit.id, 'Delete Workspace')
    
    return render_template('dashboard.html', user_fullName = current_user.full_name, workspaces = current_user.workspaces,
                           delete_form = _delete_form)

@admin_bp.route("/create_workspace", methods =["GET","POST"])
@login_required
def create_workspace():
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        return redirect(url_for('clientRoutes.client_homepage'))
    
    _form = form.createWorkspace() 
    
    if _form.validate_on_submit():
        workspace = Workspace(_form.workspace_name.data, current_user)
        db.session.add(workspace)
        db.session.commit()
        
        return redirect(url_for('adminRoutes.admin_homepage'))
    
    return render_template('createWorkspace.html', form = _form)

@admin_bp.post('/<int:workspace_id>/delete')
@login_required
def delete_workspace(workspace_id):
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        return redirect(url_for('clientRoutes.client_homepage'))

    if form.deleteForm(request.form).validate_on_submit():
        workspace = Workspace.query.get(int(workspace_id))

        if not workspace:
            session.pop('_flashes', None)
            flash("Error occurred while deleting a workspace", 'error-msg')
            return redirect(url_for('adminRoutes.admin_homepage'))
        
        try:
            current_workspace_members = WorkspaceMembers.query.filter(WorkspaceMembers.workspace_id==workspace_id).all()
            for member in current_workspace_members:
                db.session.delete(member)
            db.session.delete(workspace)
            db.session.commit()
            session.pop('_flashes', None)
            flash("Successfully deleted a workspace", 'success-msg')
        except:
            session.pop('_flashes', None)
            flash("Error occurred while deleting workspace", 'error-msg')
    return redirect(url_for('adminRoutes.admin_homepage'))
     
    

@admin_bp.route('/<int:workspace_id>/edit_workspace', methods = ["GET","POST"])
@login_required
def edit_workspace(workspace_id):

    """
        This route is responsible for editing the workspace of the admin. An admin can 
        update the name of the workspace, add an existing user in the workspace, remove
        a member of the workspace.
        
        Post requests for add and remove members are on a different route
    """

    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        return redirect(url_for('clientRoutes.client_homepage'))

    workspace = Workspace.query.get(int(workspace_id))

    if not workspace:
        session.pop('_flashes', None)
        flash("Error occurred while editing a workspace", 'error-msg')
        return redirect(url_for('adminRoutes.admin_homepage'))

    # Query all current members of the workspace given an 
    current_workspace_members = WorkspaceMembers.query.filter(WorkspaceMembers.workspace_id==workspace_id)

    # All forms for this page are instantiated here
    _updateNameForm = form.createWorkspace()
    _updateNameForm.submit.label = Label(_updateNameForm.submit.id, 'Save Workspace Name')

    _new_member_form = form.addMemberWorkspaceForm()
    
    # Dynamically change the submit button for the delete form button
    _remove_member = form.deleteForm()
    _remove_member.submit.label = Label(_remove_member.submit.id, 'Remove Member')

    # Validate if the user tries to modify the workspace name
    if _updateNameForm.validate_on_submit():
        # TODO: workspace name input validation
        workspace.workspace_name = _updateNameForm.workspace_name.data
        db.session.commit()
        session.pop('_flashes', None)
        flash("Successfully changed the workspace name", 'success-msg')
        return redirect(url_for('adminRoutes.edit_workspace', workspace_id=workspace_id))
    
    return render_template('editWorkspace.html',workspace=workspace, workspace_id=workspace_id, updateWorkspaceNameForm = _updateNameForm, new_member_form = _new_member_form, 
                          workspace_members = current_workspace_members, remove_member_form = _remove_member)

@admin_bp.post('/<int:workspace_id>/edit_workspace/add_member')
@login_required
def add_member(workspace_id):
    """
        Post validation to add a member in the workspace
    """

    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        return redirect(url_for('clientRoutes.client_homepage'))

    workspace = Workspace.query.get(int(workspace_id))
    if not workspace:
        session.pop('_flashes', None)
        flash("Error occurred while editing a workspace", 'error-msg')
        return redirect(url_for('adminRoutes.admin_homepage'))

    # Get the form submitted for new_member_form
    add_member_form = form.addMemberWorkspaceForm(request.form)
    
    # Validate if the user tries to add a new member to the workspace  
    if add_member_form.validate_on_submit():
        # TODO: Input validation
        
        # Get the new user that the admin is trying to add
        user = User.query.filter_by(email=add_member_form.email_address.data).first()

        if not user:
            session.pop('_flashes', None)
            flash("Cannot add a user that does not exist.", 'error-msg')
            return redirect(url_for('adminRoutes.edit_workspace', workspace_id=workspace_id))
        
        
        # If the entered email address is already in the workspace, flash an error
        for member in workspace.members:
            #print(member.member_id)
            if member.member_id == user.id:
                session.pop('_flashes', None)
                flash("Cannot add a user that is already part of the workspace.", 'error-msg')
                return redirect(url_for('adminRoutes.edit_workspace', workspace_id=workspace_id))
            
        # If the query returns a result save the the member to the workspace_members table
        new_member = WorkspaceMembers(workspace, user)
        db.session.add(new_member)
        db.session.commit()
        session.pop('_flashes', None)
        flash("Successfully added a user to the workspace.", 'success-msg')
    return redirect(url_for('adminRoutes.edit_workspace', workspace_id=workspace_id))

@admin_bp.post('/<int:workspace_id>/edit_workspace/remove_member/<int:member_id>')
@login_required
def remove_member(workspace_id, member_id):    
    """
        Post validation to remove a member in the workspace
    """

    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        return redirect(url_for('clientRoutes.client_homepage'))

    remove_member_form = form.deleteForm()
    if remove_member_form.validate_on_submit():
        workspace = Workspace.query.get(int(workspace_id))

        if not workspace:
            session.pop('_flashes', None)
            flash("Error occurred while editing a workspace", 'error-msg')
            return redirect(url_for('adminRoutes.admin_homepage'))

        try:
            member = WorkspaceMembers.query.filter(WorkspaceMembers.member_id==member_id, WorkspaceMembers.workspace_id==workspace.workspace_id).first()
            db.session.delete(member)
            db.session.commit()
            session.pop('_flashes', None)
            flash("Successfully removed a member", 'success-msg')
        except:
            session.pop('_flashes', None)
            flash("Error occurred while removing a member", 'error-msg')
    return redirect(url_for('adminRoutes.edit_workspace', workspace_id=workspace_id))

@admin_bp.route('/<int:workspace_id>/new_task', methods=["GET","POST"])
@login_required 
def create_task(workspace_id):
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        return redirect(url_for('clientRoutes.client_homepage'))

    _new_task_form = form.NewTask()
    workspace = Workspace.query.get(int(workspace_id))

    if not workspace:
            session.pop('_flashes', None)
            flash("Error occurred while creating a task for a workspace", 'error-msg')
            return redirect(url_for('adminRoutes.admin_homepage'))
    
    if _new_task_form.validate_on_submit():
        assigned_user =  User.query.filter_by(User.email==_new_task_form.email_address.data)
    
        if not assigned_user:
            session.pop('_flashes',None)
            flash('User does not exist','error-msg')
            return redirect(url_for('adminRoutes.create_task', workspace_id = workspace_id))
        
        #TODO: add task backend

        session.pop('_flashes', None)
        flash('Successfully created a task', 'success-msg')
        return redirect(url_for('adminRoutes.open_workspace',workspace_id = workspace_id))

    
    return render_template('createTask.html',new_task_form = _new_task_form,
                           workspace_id = workspace_id)
