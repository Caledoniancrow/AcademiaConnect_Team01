from email.mime import application
from flask import Blueprint


auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)

application_bp = Blueprint('application', __name__)
milestone_bp = Blueprint('milestone', __name__)
admin_bp = Blueprint('admin_bp', __name__)

from . import auth_routes, main_routes, application_routes, milestone_routes, admin_routes
