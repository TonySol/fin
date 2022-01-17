"""Root package. Initialises flask web app via start_app method

Holds subpackages:
– `migrations`: holds migration files to manage DB schemas
– `models`: holds DB models in form of classes
– `rest`: holds modules with REST API implementation
– `service`: holds modules with classes to work with DB and validate user input
– `static`: holds static files (e.g. scripts and css) for web app
– `templates`: holds html-templates for a web app
– `test`: holds modules with unittests
– `views`: holds modules with web controllers

"""

import logging
import sys
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def start_app(config_option):
    """Initialises web app using factory pattern.

    Registers flask blueprints. Configures logging.

    :param config_option: accepts configuration in form of object (class) to supply app on start
    :type config_option: class `config`

    :return: the flask web app instance

    All extensions are supplied with app withing the function.
    No worries about flask application-specific states stored on a "global" extension.
    The one extension object is bound only to the exactly one flask app with its specific states.
    """

    # pylint: disable=import-outside-toplevel, no-member

    app = Flask(__name__)
    app.config.from_object(config_option)

    db.init_app(app)
    migrate.init_app(app, db, directory="app/migrations")

    from app.views import web
    app.register_blueprint(web)

    from app.rest import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    if config_option.__name__ == "Config":
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

        file_handler = RotatingFileHandler('app/logs/fin.log', maxBytes=51200, backupCount=3)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        cli_handler = logging.StreamHandler(sys.stdout)
        cli_handler.setFormatter(formatter)
        cli_handler.setLevel(logging.DEBUG)

        app.logger.addHandler(file_handler)
        app.logger.addHandler(cli_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Fin_project started')

    return app
