from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed, FileField, FileSize
from flask_wtf.recaptcha import RecaptchaField
from PIL import Image

class RegistrationForm(FlaskForm):
    recaptcha = RecaptchaField()
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif']), FileSize(max_size=1000000)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=13)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=12, max=64)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=12, max=64)])
    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Login')

class createWorkspace(FlaskForm):
    workspace_name = StringField('Workspace Name', validators=[DataRequired(), Length(min=1,max=120)])
    submit = SubmitField('Save Workspace')

class deleteForm(FlaskForm):
    submit = SubmitField()
