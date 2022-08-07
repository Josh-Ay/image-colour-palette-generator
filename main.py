from app import create_flask_app
from app.flask_app_config import DevelopmentConfig, ProductionConfig
from app.routes_blueprint.users_blueprint import users_blueprint
from app.routes_blueprint.home_blueprint import home_blueprint
from app.routes_blueprint.authentication_blueprints import authentication_blueprint
from app.error_handlers.error_routes import handle_page_not_found, handle_unauthorized_access
from app.robots_text_handler.robots_text_handler import robots_text_blueprint

# creating a new flask application
app = create_flask_app(ProductionConfig())

# registering blueprints/views for the flask application
app.register_blueprint(home_blueprint, url_prefix="/")
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(authentication_blueprint, url_prefix="/oauth")
app.register_blueprint(robots_text_blueprint, url_prefix="")

# registering error handlers for the flask application
app.register_error_handler(403, handle_unauthorized_access)
app.register_error_handler(404, handle_page_not_found)


if __name__ == "__main__":
    app.run()
