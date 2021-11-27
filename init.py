from flask import Flask, render_template, url_for, request, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = "dslkfneklf3pojfkojdenvfp03023rn"

from views.routes import go

app.register_blueprint(go)

if __name__ == "__main__":
    app.run(debug=True)
