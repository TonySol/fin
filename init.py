"""Ignition file: starts flask, apps, prepares env, gets routes, db

Env: you can choose production class or dev(uses Public HOST) class
Routes: api routes via blueprint, user via methos aka constructor
"""

from flask import Flask
from flask_jwt_extended import JWTManager

#importing routes
import config
from views.routes import routes
from views.api_routes import api

#instatiate apps
app = Flask(__name__)
jwt = JWTManager(app)

#get config
app.config.from_object(config.Development)

#registering routes
routes(app)
app.register_blueprint(api, url_prefix="/api")


if __name__ == "__main__":
    app.run(host=app.config.get("HOST"))
