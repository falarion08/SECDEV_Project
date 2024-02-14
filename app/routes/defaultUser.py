from flask import render_template, request, flash, redirect, jsonify, url_for, make_response
import flask_login
from flask_login import login_user, logout_user
from app.models import db
from app.models.User import User
from app.controllers import userController
from . import defaultUser_bp,login_manager
from .main import current_user



@defaultUser_bp.route('/', methods=["GET", "POST"])
def defaultUserHomepage():
    print(f'\n\n{current_user.is_authenticated}\n\n')
    if (current_user.is_authenticated):
        return render_template('index.html')
    else:
        return redirect('/')
    
@defaultUser_bp.route('/logout', methods=["GET", "POST"])
def logout_user():
    logout_user()
    return redirect('/')
