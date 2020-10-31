from flask import Flask
from .config import config_by_name

from .models import db

from .views.users import user_api


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

    app.register_blueprint(user_api, url_prefix='/api/v1')

    return app
