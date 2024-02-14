import os

def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Set to false to use less memory
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = 'cssecdvSECRETKEY'
    app.config['UPLOAD_FOLDER'] = os.getenv('FOLDER_UPLOAD')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_IMAGE_SIZE')) # 1MB Max
    