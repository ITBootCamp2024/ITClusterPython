from flask import Flask, render_template
from routes.db_healthchecker import db_health

app = Flask(__name__)
app.register_blueprint(db_health)


@app.route('/')
def hello_world():
    return render_template('index.html', title="ITClusterPython2024")


if __name__ == "__main__":
    app.run(debug=True)
