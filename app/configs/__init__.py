def setup_db(app, url, upload_folder):
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Set to false to use less memory
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['UPLOAD_FOLDER'] = upload_folder
