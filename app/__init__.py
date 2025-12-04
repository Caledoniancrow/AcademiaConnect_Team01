from flask import Flask
# We will import config from the outer folder
# Note: We need to modify sys path or just import Config if it's in root
# Standard way for this structure:
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # We will add database and routes later
    @app.route('/')
    def hello():
        return "Academia Connect is Running!"

    return app