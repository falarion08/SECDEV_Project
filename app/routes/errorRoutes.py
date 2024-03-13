from flask import render_template, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from app.models.User import db, User
from . import error_bp

"""
    This file is dedicated for views that are made available for each possible error in the website
"""

@error_bp.app_errorhandler(404)
def error_404(e):
    return render_template(
        'errorPage.html',
        error_num=404,
        error_text="Page Not Found"), 404

@error_bp.app_errorhandler(500)
def error_500(e):
    return render_template(
        'errorPage.html',
        error_num=500,
        error_text="Internal Server Error"), 500

@error_bp.app_errorhandler(413)
def error_413(e):
    return render_template(
        'errorPage.html',
        error_num=413,
        error_text="Request Entity Too Large"), 413

@error_bp.app_errorhandler(429)
def error_429(e):
    return render_template(
        'errorPage.html',
        error_num=429,
        error_text="Too Many Requests"), 429
    
