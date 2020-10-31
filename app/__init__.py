from flask import Flask
from .config import config_by_name

from .models import db


def create_app(config_name: str) -> Flask:
    # app initialization
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # initialize db
    db.init_app(app)

    # for health check
    @app.route('/', methods=['GET'])
    def ping():
        return 'pong'

    return app
