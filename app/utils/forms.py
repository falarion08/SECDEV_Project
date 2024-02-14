from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.file import FileAllowed, FileField, FileSize
from PIL import Image

def is_image(form, field):
    if field.data:
        img = Image.open(field.data)
        if img.format.lower() not in ['jpg', 'jpeg', 'png', 'gif']:
            raise ValidationError('Invalid image format. Supported formats: JPEG, JPG, PNG, GIF')

def is_small_enough(form, field):
    if field.data:
        max_size_in_bytes = 1 * 1024 * 1024
        if len(field.data.read()) > max_size_in_bytes:
            raise ValidationError('Image size exceeds the maximum allowed (1MB)')

class RegistrationForm(FlaskForm):
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
    submit = SubmitField('Login')