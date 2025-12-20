from flask import Flask
import sys
import os

# Ensure we can import config from the root folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Database
    from . import db
    db.init_app(app)

    # --- IMPORT BLUEPRINTS ---
    # We import these LOCALLY to avoid circular import errors
    from .controllers.auth_routes import auth_bp
    from .controllers.main_routes import main_bp
    from .controllers.application_routes import application_bp  # <--- NEW
    from .controllers.milestone_routes import milestone_bp      # <--- NEW
    
    # --- REGISTER BLUEPRINTS ---
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(application_bp)  # <--- Connects the Application/Faculty logic
    app.register_blueprint(milestone_bp)    # <--- Connects the Grading/Milestone logic

    return app