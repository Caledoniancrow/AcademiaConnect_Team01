from flask import Flask
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from . import db
    db.init_app(app)

    from .controllers import auth_bp, main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
