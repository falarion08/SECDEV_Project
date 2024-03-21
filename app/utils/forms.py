from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, DateField, TextAreaField  
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed, FileField, FileSize
from flask_wtf.recaptcha import RecaptchaField
from PIL import Image
from datetime import datetime
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

class addMemberWorkspaceForm(FlaskForm):
    email_address = StringField('Add Member', validators=[DataRequired(),Length(min = 12,max=64)])
    submit = SubmitField('Add Member')
    
class NewTask(FlaskForm):
    task_name= StringField('Task Name', validators=[DataRequired(),Length(min=1,max=80)])
    email_address = StringField('Assigned User', validators=[DataRequired(),Length(min=12,max=64)]) 
    due_date  = DateField('Due Date')
    submit = SubmitField('Save Task')

class UpdateDueDateForm(FlaskForm):
    due_date = DateField('Due Date')
    submit = SubmitField('Save Due Date')

class NewUpdate(FlaskForm):
    update = TextAreaField('Update', validators=[DataRequired(),Length(min=1,max=256)])
    submit = SubmitField('Submit Update')


    

    