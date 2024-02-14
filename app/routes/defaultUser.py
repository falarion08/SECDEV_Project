from flask import render_template, request, flash, redirect, jsonify, url_for, make_response
import flask_login
from flask_login import login_user, logout_user,current_user
from app.models import db
from app.models.User import User
from app.controllers import userController
from . import defaultUser_bp, errors,login_manager

@login_manager.user_loader
def load_user(user_email):
    return User.query.filter_by(email=user_email)

@defaultUser_bp.route('/default', methods=["GET", "POST"])
def defaultUserHomepage():
    return render_template('index.html')