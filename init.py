from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = "dslkfneklf3pojfkojdenvfp03023rn"


from views.routes import start_app
start_app(app)


from views.api_routes import api
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
