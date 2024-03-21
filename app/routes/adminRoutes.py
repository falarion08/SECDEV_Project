from flask import render_template, flash, redirect, url_for, session,request
from flask_login import login_required, current_user
from app.models.User import db, User
from . import admin_bp,login_manager
from app.controllers import verify_email, verify_title
from app.models.Task import Task
from app.models.Workspace import Workspace
from app.models.WorkspaceMembers import WorkspaceMembers
from app.models.Task import Task
from  wtforms import Label
import app.utils.forms as form
import logging

logging.basicConfig(filename='sys.log', filemode='a', format='%(asctime)s  %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)


# Required decorator when using flask-login to find authenticated user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@admin_bp.route('/admin', methods=["GET"])
@login_required
def admin_homepage():
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        logging.warning(f'An unauthenticated user tried to access /admin')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        logging.warning(f'[{current_user.email} - {current_user.role}] tried to access /admin')
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
        logging.warning(f'An unauthenticated user tried to access /create_workspace')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        logging.warning(f'[{current_user.email} - {current_user.role}] tried to access /create_workspace')
        return redirect(url_for('clientRoutes.client_homepage'))
    
    _form = form.createWorkspace() 
    
    if _form.validate_on_submit():
        workspace = Workspace(_form.workspace_name.data, current_user)
        db.session.add(workspace)
        db.session.commit()
        logging.info(f'[{current_user.email} - {current_user.role}] has created a new workspace [{workspace.workspace_id} - {workspace.workspace_name}]')
        return redirect(url_for('adminRoutes.admin_homepage'))
    
    return render_template('createWorkspace.html', form = _form)


@admin_bp.post('/<int:workspace_id>/delete')
@login_required
def delete_workspace(workspace_id):
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        logging.warning(f'An unauthenticated user tried to access /delete')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        logging.warning(f'[{current_user.email} - {current_user.role}] tried to access /delete')
        return redirect(url_for('clientRoutes.client_homepage'))

    if form.deleteForm(request.form).validate_on_submit():
        workspace = Workspace.query.get(int(workspace_id))

        if not workspace:
            session.pop('_flashes', None)
            flash("Error occurred while deleting a workspace", 'error-msg')
            return redirect(url_for('adminRoutes.admin_homepage'))
        
        try:
            current_workspace_members = WorkspaceMembers.query.filter(WorkspaceMembers.workspace_id==workspace_id).all()
            workspace_name = workspace.workspace_name
            for member in current_workspace_members:
                db.session.delete(member)
            db.session.delete(workspace)
            db.session.commit()
            session.pop('_flashes', None)
            flash("Successfully deleted a workspace", 'success-msg')
            logging.info(f'[{current_user.email} - {current_user.role}] deleted workspace [{workspace_id} - {workspace_name}]')
        except:
            session.pop('_flashes', None)
            flash("Error occurred while deleting workspace", 'error-msg')
            logging.warning(f'[{current_user.email} - {current_user.role}] attempted to delete workspace [ID: {workspace_id}]')
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
        logging.warning(f'An unauthenticated user tried to access /edit_workspace')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        logging.warning(f'[{current_user.email} - {current_user.role}] tried to access /edit_workspace')
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
        is_workspace_name_valid = verify_title(_updateNameForm.workspace_name.data)
        if not is_workspace_name_valid:
            session.pop('_flashes', None)
            flash("Please enter a valid workspace name", 'error-msg')
            logging.info(f'[{current_user.email} - {current_user.role}] tried to change the workspace name of [{workspace.workspace_id} - {workspace.workspace_name}]')
            return redirect(url_for('adminRoutes.edit_workspace', workspace_id=workspace_id))

        original_name = workspace.workspace_name
        workspace.workspace_name = _updateNameForm.workspace_name.data
        db.session.commit()
        session.pop('_flashes', None)
        flash("Successfully changed the workspace name", 'success-msg')
        logging.info(f'[{current_user.email} - {current_user.role}] changed the workspace name of [{original_name}] to [{_updateNameForm.workspace_name.data}]')
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
        logging.warning(f'An unauthenticated user tried to access /add_member')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        logging.warning(f'[{current_user.email} - {current_user.role}] tried to access /add_member')
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
        is_email_valid = verify_email(add_member_form.email_address.data)
        if not is_email_valid:
            session.pop('_flashes', None)
            flash("Please enter a valid email.", 'error-msg')
            logging.warning(f'[{current_user.email} - {current_user.role}] tried to add a user [{add_member_form.email_address.data}] to workspace [{workspace.workspace_id} - {workspace.workspace_name}]')
            return redirect(url_for('adminRoutes.edit_workspace', workspace_id=workspace_id))


        # Get the new user that the admin is trying to add
        user = User.query.filter_by(email=add_member_form.email_address.data).first()

        if not user:
            session.pop('_flashes', None)
            flash("Cannot add a user that does not exist.", 'error-msg')
            logging.warning(f'[{current_user.email} - {current_user.role}] tried to add a user [{add_member_form.email_address.data}] to workspace [{workspace.workspace_id} - {workspace.workspace_name}]')
            return redirect(url_for('adminRoutes.edit_workspace', workspace_id=workspace_id))
        
        
        # If the entered email address is already in the workspace, flash an error
        for member in workspace.members:
            #print(member.member_id)
            if member.member_id == user.id:
                session.pop('_flashes', None)
                flash("Cannot add a user that is already part of the workspace.", 'error-msg')
                logging.warning(f'[{current_user.email} - {current_user.role}] tried to add existing workspace member [{add_member_form.email_address.data}] to workspace [{workspace.workspace_id} - {workspace.workspace_name}]')
                return redirect(url_for('adminRoutes.edit_workspace', workspace_id=workspace_id))
            
        # If the query returns a result save the the member to the workspace_members table
        new_member = WorkspaceMembers(workspace, user)
        db.session.add(new_member)
        db.session.commit()
        session.pop('_flashes', None)
        flash("Successfully added a user to the workspace.", 'success-msg')
        logging.info(f'[{current_user.email} - {current_user.role}] added user [{add_member_form.email_address.data}] to workspace [{workspace.workspace_id} - {workspace.workspace_name}]')
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
        logging.warning(f'An unauthenticated user tried to access /remove_member')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        logging.warning(f'[{current_user.email} - {current_user.role}] tried to access /remove_member')
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
            member_email = member.member_details.email
            db.session.delete(member)
            db.session.commit()
            session.pop('_flashes', None)
            flash("Successfully removed a member", 'success-msg')
            logging.info(f'[{current_user.email} - {current_user.role}] removed user [{member_email}] from workspace [{workspace.workspace_id} - {workspace.workspace_name}]')
        except:
            session.pop('_flashes', None)
            flash("Error occurred while removing a member", 'error-msg')
            logging.info(f'[{current_user.email} - {current_user.role}] tried to removed user [{member_email}] from workspace [{workspace.workspace_id} - {workspace.workspace_name}]')
    return redirect(url_for('adminRoutes.edit_workspace', workspace_id=workspace_id))

@admin_bp.route('/<int:workspace_id>/new_task', methods=["GET", "POST"])
@login_required 
def create_task(workspace_id):
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        logging.warning(f'An unauthenticated user tried to access /new_task')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        logging.warning(f'[{current_user.email} - {current_user.role}] tried to access /new_task')
        return redirect(url_for('clientRoutes.client_homepage'))

    _new_task_form = form.NewTask()
    workspace = Workspace.query.get(int(workspace_id))

    if not workspace:
            session.pop('_flashes', None)
            flash("Error occurred while creating a task for a workspace", 'error-msg')
            return redirect(url_for('adminRoutes.admin_homepage'))
    
    if _new_task_form.validate_on_submit():
        user =  User.query.filter_by(email=_new_task_form.email_address.data).first()

        if not user:
            session.pop('_flashes',None)
            flash('User does not exist','error-msg')
            return redirect(url_for('adminRoutes.create_task', workspace_id = workspace_id))
        
        member = WorkspaceMembers.query.filter(WorkspaceMembers.member_id==user.id, WorkspaceMembers.workspace_id==workspace.workspace_id).first()
        if not member:
            session.pop('_flashes', None)
            flash("Assigned user must be a part of the workspace.", 'error-msg')
            return redirect(url_for('adminRoutes.create_task', workspace_id=workspace_id))

        is_valid_task_name = verify_title(_new_task_form.task_name.data)
        if not is_valid_task_name:
            session.pop('_flashes',None)
            flash('Task name is invalid','error-msg')
            return redirect(url_for('adminRoutes.create_task', workspace_id = workspace_id))
    
        task = Task(_new_task_form.task_name.data,_new_task_form.email_address.data,_new_task_form.due_date.data, _new_task_form.status.data, workspace, user)
        db.session.add(task)
        db.session.commit()
        session.pop('_flashes', None)
        flash('Successfully created a task', 'success-msg')
        logging.info(f'[{current_user.email} - {current_user.role}] created a task [{task.task_id} - {task.task_name}]')
        return redirect(url_for('clientRoutes.open_workspace',workspace_id = workspace_id))

    return render_template('createTask.html', new_task_form=_new_task_form, workspace_id = workspace_id)

@admin_bp.post('/<int:workspace_id>/<int:task_id>/edit_task/edit_task_name')
@login_required
def edit_task_name(workspace_id, task_id):
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        logging.warning(f'An unauthenticated user tried to access /edit_task_name')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        logging.warning(f'[{current_user.email} - {current_user.role}] tried to access /edit_task_name')
        return redirect(url_for('clientRoutes.client_homepage'))

    workspace = Workspace.query.get(int(workspace_id))
    if not workspace:
        session.pop('_flashes', None)
        flash("Error occurred while editing a workspace", 'error-msg')
        return redirect(url_for('adminRoutes.admin_homepage'))
    
    task = Task.query.get(int(task_id))
    if not task:
        session.pop('_flashes', None)
        flash("Error occurred while editing a task", 'error-msg')
        return redirect(url_for('clientRoutes.open_workspace', workspace_id=workspace_id))

    _updateTaskForm = form.createWorkspace(request.form)
    
    if _updateTaskForm.validate_on_submit():
        is_valid_task_name = verify_title(_updateTaskForm.workspace_name.data)
        if not is_valid_task_name:
            session.pop('_flashes',None)
            flash('Task name is invalid','error-msg')
            return redirect(url_for('clientRoutes.edit_task', workspace_id = workspace_id))

        task.task_name = _updateTaskForm.workspace_name.data
        db.session.commit()
        session.pop('_flashes', None)
        flash("Successfully changed the task name", 'success-msg')
        return redirect(url_for('clientRoutes.edit_task', workspace_id=workspace_id, task_id=task_id))
    
    return redirect(url_for('clientRoutes.edit_task', workspace_id=workspace_id, task_id=task_id))

@admin_bp.post('/<int:workspace_id>/<int:task_id>/edit_task/edit_task_assigned_user')
@login_required
def edit_task_assigned_user(workspace_id, task_id):
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        logging.warning(f'An unauthenticated user tried to access /edit_task_assigned_user')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        logging.warning(f'[{current_user.email} - {current_user.role}] tried to access /edit_task_assigned_user')
        return redirect(url_for('clientRoutes.client_homepage'))

    workspace = Workspace.query.get(int(workspace_id))
    if not workspace:
        session.pop('_flashes', None)
        flash("Error occurred while editing a workspace", 'error-msg')
        return redirect(url_for('adminRoutes.admin_homepage'))

    task = Task.query.get(int(task_id))
    if not task:
        session.pop('_flashes', None)
        flash("Error occurred while editing a task", 'error-msg')
        return redirect(url_for('clientRoutes.open_workspace', workspace_id=workspace_id))

    _updateAssignedUserForm = form.addMemberWorkspaceForm(request.form)
    
    if _updateAssignedUserForm.validate_on_submit():
        is_valid_assigned_user_email = verify_email(_updateAssignedUserForm.email_address.data)
        if not is_valid_assigned_user_email:
            session.pop('_flashes',None)
            flash('Assigned User email is invalid','error-msg')
            return redirect(url_for('clientRoutes.edit_task', workspace_id = workspace_id))
        
        user = User.query.filter_by(email=_updateAssignedUserForm.email_address.data).first()
        if not user:
            session.pop('_flashes', None)
            flash("Cannot add a user that does not exist.", 'error-msg')
            logging.warning(f'[{current_user.email} - {current_user.role}] tried to assign [{_updateAssignedUserForm.email_address.data}] to task [{task.task_id} - {task.task_name}]')
            return redirect(url_for('clientRoutes.edit_task', workspace_id=workspace_id, task_id=task_id))
        
        member = WorkspaceMembers.query.filter(WorkspaceMembers.member_id==user.id, WorkspaceMembers.workspace_id==workspace.workspace_id).first()
        if not member:
            session.pop('_flashes', None)
            flash("Assigned user must be a part of the workspace.", 'error-msg')
            logging.warning(f'[{current_user.email} - {current_user.role}] tried to assign [{_updateAssignedUserForm.email_address.data}] to task [{task.task_id} - {task.task_name}]')
            return redirect(url_for('clientRoutes.edit_task', workspace_id=workspace_id, task_id=task_id))
        

        if task.assigned_user_email_address == _updateAssignedUserForm.email_address.data:
            session.pop('_flashes',None)
            flash('User is already assigned for this task!','error-msg')
            return redirect(url_for('clientRoutes.edit_task',workspace_id=workspace_id, task_id=task_id))

        new_assigned_user = User.query.filter_by(email=_updateAssignedUserForm.email_address.data).first()
        
        logging.info(f'[{current_user.email} - {current_user.role}] reassigned {task.assigned_user_email_address} to {new_assigned_user.email} in Task_id: {task_id} from workspace_id: {workspace_id}')     
           
        task.assigned_user_email_address =_updateAssignedUserForm.email_address.data
        task.user_assigned_details = new_assigned_user
        

        db.session.commit()
        session.pop('_flashes', None)
        flash("Successfully changed the task assigned user", 'success-msg')
        return redirect(url_for('clientRoutes.edit_task', workspace_id=workspace_id, task_id=task_id))
    
    return redirect(url_for('clientRoutes.edit_task', workspace_id=workspace_id, task_id=task_id))

@admin_bp.post('/<int:workspace_id>/<int:task_id>/edit_task/edit_task_due_date')
@login_required
def edit_task_due_date(workspace_id, task_id):
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        logging.warning(f'An unauthenticated user tried to access /edit_task_due_date')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        logging.warning(f'[{current_user.email} - {current_user.role}] tried to access /edit_task_due_date')
        return redirect(url_for('clientRoutes.client_homepage'))

    workspace = Workspace.query.get(int(workspace_id))
    if not workspace:
        session.pop('_flashes', None)
        flash("Error occurred while editing a workspace", 'error-msg')
        return redirect(url_for('adminRoutes.admin_homepage'))
    
    task = Task.query.get(int(task_id))
    if not task:
        session.pop('_flashes', None)
        flash("Error occurred while editing a task", 'error-msg')
        return redirect(url_for('clientRoutes.open_workspace', workspace_id=workspace_id))

    _updateDueDateForm = form.UpdateDueDateForm(request.form)
    
    if _updateDueDateForm.validate_on_submit():
        task.due_date = _updateDueDateForm.due_date.data
        db.session.commit()
        session.pop('_flashes', None)
        flash("Successfully changed the task due date", 'success-msg')
        return redirect(url_for('clientRoutes.edit_task', workspace_id=workspace_id, task_id=task_id))
                                
    return redirect(url_for('clientRoutes.edit_task', workspace_id=workspace_id, task_id=task_id))

@admin_bp.post('/<int:workspace_id>/<int:task_id>/delete_task')
@login_required
def delete_task(workspace_id, task_id):
    if not current_user.is_authenticated:
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        logging.warning(f'An unauthenticated user tried to access /delete')
        return redirect(url_for('landingRoutes.login_page'))
    
    if current_user.role != 'admin':
        session.pop('_flashes', None)
        flash('You must be authorized to access this page!', 'error-msg')
        logging.warning(f'[{current_user.email} - {current_user.role}] tried to access /delete')
        return redirect(url_for('clientRoutes.client_homepage'))
    
    workspace = Workspace.query.get(int(workspace_id))
    if not workspace:
        session.pop('_flashes', None)
        flash("Error occurred while deleting a workspace", 'error-msg')
        return redirect(url_for('adminRoutes.admin_homepage'))
    
    task = Task.query.get(int(task_id))
    if not task:
        session.pop('_flashes', None)
        flash("Error occurred while deleting a task", 'error-msg')
        return redirect(url_for('clientRoutes.open_task_updates', workspace_id=workspace_id, task_id=task_id))
    
    _deleteTaskForm = form.deleteForm(request.form)
    if _deleteTaskForm.validate_on_submit():
        try:
            task_name = task.task_name
            db.session.delete(task)
            db.session.commit()
            session.pop('_flashes', None)
            flash("Successfully deleted a task", 'success-msg')
            logging.info(f'[{current_user.email} - {current_user.role}] deleted task [{task_id} - {task_name}]')
        except:
            session.pop('_flashes', None)
            flash("Error occurred while deleting workspace", 'error-msg')
            logging.warning(f'[{current_user.email} - {current_user.role}] attempted to delete task [ID: {task_id}]')
    return redirect(url_for('clientRoutes.open_workspace', workspace_id=workspace_id))