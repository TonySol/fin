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
    app = Flask(__name__)
    app.config.from_object(config_option)

    db.init_app(app)
    migrate.init_app(app, db, directory="app/migrations")

    from app.views import web
    app.register_blueprint(web)

    from app.rest import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")


    if config_option.__name__ == "Config":
        file_handler = RotatingFileHandler('fin.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Fin_project started')

    return app


# def create_db(app):
#     with app.app_context():
#         db.create_all()
#     dept = Department()
#     dept.name = "Asus"
#     db.session.add(dept)
#     db.session.commit()
