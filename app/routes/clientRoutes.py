from flask import render_template, flash, redirect, url_for, session,request
from flask_login import login_required, current_user
from app.models.User import db, User
from . import client_bp, login_manager
from app.models.Task import Task
from app.models.TaskUpdates import TaskUpdates
from app.models.Workspace import Workspace
from app.models.WorkspaceMembers import WorkspaceMembers
from  wtforms import Label
import app.utils.forms as form

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@client_bp.route('/dashboard', methods=["GET", "POST"])
@login_required
def client_homepage():
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        return redirect(url_for('landingRoutes.login_page'))
    
    _workspaces = []
    for member in current_user.workspaces_member_of:
        _workspaces.append(member.workspace)

    return render_template('dashboard.html', user_fullName = current_user.full_name, workspaces=_workspaces)

@client_bp.route("/<int:workspace_id>", methods =["GET","POST"])
@login_required
def open_workspace(workspace_id):
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        return redirect(url_for('landingRoutes.login_page'))

    workspace = Workspace.query.get(int(workspace_id))
    if not workspace:
        session.pop('_flashes', None)
        flash("Error occurred while accessing a workspace", 'error-msg')
        return redirect(url_for('adminRoutes.admin_homepage'))
    
    return render_template('Workspace.html', workspace_id=workspace_id, workspace=workspace)

@client_bp.route('/<int:workspace_id>/<int:task_id>/updates/', methods=["GET","POST"])
@login_required 
def open_task_updates(workspace_id, task_id):
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        return redirect(url_for('landingRoutes.login_page'))

    workspace = Workspace.query.get(int(workspace_id))
    update_form = form.NewUpdate()
    task = Task.query.get(int(task_id))
    
    _delete_update_form = form.deleteForm()
    _delete_update_form.submit.label = Label(_delete_update_form.submit.id, "Delete")

    _delete_task_form = form.deleteForm()
    _delete_task_form.submit.label = Label(_delete_task_form.submit.id, "Delete Task")

    if not workspace:
        session.pop('_flashes', None)
        flash("Error occurred while accessing a workspace", 'error-msg')
        return redirect(url_for('adminRoutes.admin_homepage'))
    if not task:
        session.pop('_flashes', None)
        flash("Error occurred while accessing a task", 'error-msg')
        return redirect(url_for('clientRoutes.open_workspace', workspace_id=workspace_id))

    if update_form.validate_on_submit():
        task_update = TaskUpdates(update_form.update.data,current_user,task)
        db.session.add(task_update)
        db.session.commit()
        return redirect(url_for('clientRoutes.open_task_updates',workspace_id=workspace_id, task_id=task_id))
        
    return render_template('Task.html', workspace_id=workspace_id, task_id=task_id, form=update_form, task=task,view_mode = "UPDATE"
                           , delete_update_form = _delete_update_form, delete_task_form=_delete_task_form)

@client_bp.post('/<int:workspace_id>/task/updates/<int:task_id>/<int:update_id>/delete_update')
@login_required
def delete_update(workspace_id,task_id,update_id):
    
    _deleteUpdateForm = form.deleteForm(request.form)
    if _deleteUpdateForm.validate_on_submit():
        try:
            db.session.delete(TaskUpdates.query.get(int(update_id)))
            db.session.commit()
            session.pop('_flashes', None)
            flash("Successfully deleted an update", 'success-msg')
        except:
            session.pop('_flashes', None)
            flash("An error occured while deleting an update", 'error-msg')

    return redirect(url_for('clientRoutes.open_task_updates', workspace_id=workspace_id,task_id = task_id))

