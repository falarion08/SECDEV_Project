from app.models import db

# user_roles = db.Table(
#     'roles_user',
#                      db.Column('user_id',db.Integer(), db.ForeignKey('users.id')),
#                      db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
#                      )