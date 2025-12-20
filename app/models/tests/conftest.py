import pytest
from app import create_app

@pytest.fixture
def app():
    # Create the app in testing mode
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for easier testing
    return app

@pytest.fixture
def client(app):
    return app.test_client()