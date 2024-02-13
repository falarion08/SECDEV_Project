from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.file import FileAllowed, FileField
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
    profile_photo = FileField('Profile Photo')
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif']), is_image, is_small_enough])