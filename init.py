"""Ignition file: starts flask, apps, prepares env, gets routes, db

Env: you can choose production class or dev(uses Public HOST) class
Routes: api routes via blueprint, user via methos aka constructor
"""

from flask import Flask
from flask_jwt_extended import JWTManager

import config

jwt = JWTManager()


def start_app(config_option=config.Config):
    """This factory pattern is used to run extensions on multiple apps if needed.

    No worries about flask application-specific states stored on a "global" extension.
    The one extension object is bound only to the exactly one flask app with its specific states.
    """
    app = Flask(__name__)
    app.config.from_object(config_option)

    jwt.init_app(app)

    # importing and registering routes
    from views.routes import routes
    from views.api_routes import api

    routes(app)
    app.register_blueprint(api, url_prefix="/api")

    return app


# choose config to run
application = start_app(config.Development)

if __name__ == "__main__":
    application.run()
