import dotenv, os
dotenv.load_dotenv()

from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_compress import Compress
from flask_session import Session
from uuid import uuid4

from werkzeug.middleware.proxy_fix import ProxyFix

from .base import db


def create_app():
    app = Flask(__name__)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 3600 # cache static files
    app.config["SECRET_KEY"] = uuid4().hex
    app.template_folder = "../templates"
    app.static_folder = "../static"

    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_FILE_DIR"] = "/tmp/sessions"

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRESQL_URI"]

    CORS(app)
    Session(app)
    Compress(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.login_message = ''
    login_manager.init_app(app)

    
    from ..auth import auth_bp
    app.register_blueprint(auth_bp)

    return (app, login_manager)

