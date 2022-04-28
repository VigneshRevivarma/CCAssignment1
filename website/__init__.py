from email.mime import application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_share import Share

db = SQLAlchemy()

def create_app():
    application=app = Flask(__name__)
    app.config['SECRET_KEY'] = 'batman'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@database-1.czw5ppll5s2k.us-east-1.rds.amazonaws.com:3306/db'
    db.init_app(app)

    share = Share(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)

    return app

def create_database(app):
        db.create_all(app=app)
        print('Created Database!')