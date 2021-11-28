from flask import Flask
from flask_jwt_extended import JWTManager

from views.routes import routes
from views.api_routes import api

app = Flask(__name__)
app.config['SECRET_KEY'] = "dslkfneklf3pojfkojdenvfp03023rn"
app.config["JWT_SECRET_KEY"] = "dfsdgsdgdsg345645fwf34tgv4erf2"

jwt = JWTManager(app)

routes(app)

app.register_blueprint(api, url_prefix="/api")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
