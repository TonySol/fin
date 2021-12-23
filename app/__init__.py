"""Ignition file: starts flask, apps, prepares env, gets routes, db

:env: choose production class or dev(uses Public HOST) class
:routes: api-routes via blueprint, user-routes via method aka constructor
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def start_app(config_option):
    """This factory pattern is used to run extensions on multiple apps if needed.

    No worries about flask application-specific states stored on a "global" extension.
    The one extension object is bound only to the exactly one flask app with its specific states.
    """
    app = Flask(__name__)
    app.config.from_object(config_option)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.views import web
    app.register_blueprint(web)

    from app.views import api
    app.register_blueprint(api, url_prefix="/api")

    return app


# def create_db(app):
#     with app.app_context():
#         db.create_all()
#     dept = Department()
#     dept.name = "Asus"
#     db.session.add(dept)
#     db.session.commit()


