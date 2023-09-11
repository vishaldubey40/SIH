#__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = '/path/to/upload/folder' 
    db.init_app(app)
    # app.config['FLASH_MESSAGE_DURATION'] = 2
     

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .model import Student,Teacher,Institution,Project
    
    with app.app_context():
        db.create_all()
        

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'views.home'
    
    @login_manager.user_loader
    def load_user(user_id):
    
        if user_id is not None:
        # Try to find the user in each user model
            student = Student.query.get(user_id)
            if student:
                return student

            teacher = Teacher.query.get(user_id)
            if teacher:
                return teacher

            institution = Institution.query.get(user_id)
            if institution:
                return institution

        return None

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')