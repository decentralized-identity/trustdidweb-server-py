from flask import Flask
from config import Config
from app.errors import bp as errors_bp
from app.routes.main import bp as main_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp)

    return app