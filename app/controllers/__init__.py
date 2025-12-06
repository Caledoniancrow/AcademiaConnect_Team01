from app.controllers.auth_routes import auth_bp
from app.controllers.main_routes import main_bp



app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
