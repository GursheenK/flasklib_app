from os import error
from flask import Flask
from flasklib.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login' # for @login_required to work, the login_view must be set to the login page so that it knows what to show when admin is not logged in.
login_manager.login_message = 'Please login to view this page.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flasklib.main.routes import main
    from flasklib.members.routes import members
    from flasklib.books.routes import books
    from flasklib.issues.routes import issues
    from flasklib.errorhandlers.handlers import errorhandlers
    app.register_blueprint(main)
    app.register_blueprint(members)
    app.register_blueprint(books)
    app.register_blueprint(issues)
    app.register_blueprint(errorhandlers)

    return app