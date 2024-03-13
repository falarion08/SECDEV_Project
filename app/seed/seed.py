from app.models.User import User,db
from bcrypt import hashpw
from app.controllers import hashPassword

"""
    This file is responsible for filling the database with dummy
"""


def create_admin():
    admin_user = User.query.filter_by(role="admin").first()

    if admin_user:
        return
    password = hashPassword('asdfQWERTY1357!')
    admin_user = User(
        email='admin@admin.com',
        hash= password[1],
        salt = password[0],
        full_name = "Admin Account",
        phone_number='123456789012',
        profile_picture=None,
        role="admin"
    )
    db.session.add(admin_user)
    db.session.commit()
