from flask import render_template, flash, redirect, url_for, session,request
from flask_login import login_user, login_required, logout_user, current_user
from app.models.User import db, User
from . import client_bp, login_manager
from app.models.Task import Task
from app.models.Workspace import Workspace
from app.models.WorkspaceMembers import WorkspaceMembers
from  wtforms import Label
import app.utils.forms as form

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@client_bp.route('/', methods=["GET", "POST"])
@login_required
def client_homepage():
    if not current_user.is_authenticated: 
        session.pop('_flashes', None)
        flash('You must be logged in to access this page!', 'error-msg')
        return redirect(url_for('landingRoutes.login_page'))
    
    # need <Workspace1>, <Workspace2>, <Workspace3> from <Memer
    _workspaces = []
    for member in current_user.workspaces_member_of:
        _workspaces.append(member.workspace)
    
    return render_template('dashboard.html', user_fullName = current_user.full_name, workspaces=_workspaces)

@client_bp.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash("You have been logged out.", "success-msg")
    
    return redirect(url_for('landingRoutes.login_page'))