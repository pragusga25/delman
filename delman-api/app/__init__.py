from flask import Flask
from config import get_config
from app.exts import db, jwt, migrate
from app.routes import register_routes
from app.services import create_services
from app.utils import CustomJSONProvider

def create_app():
    app = Flask(__name__)
    app.json_provider_class = CustomJSONProvider
    app.json = CustomJSONProvider(app)
    app.config.from_object(get_config())

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Create services
    services = create_services(db)

    # Register routes
    register_routes(app, services)

    return app
