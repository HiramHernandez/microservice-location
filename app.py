import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from src.extensions import db
from src.urls import urls

app = Flask(__name__)
CORS(app)
app.config.from_json(os.path.abspath(os.path.join('settings.json')))

port = 8000 if not 'PORT' in app.config else app.config['PORT']

db.init_app(app)
app.register_blueprint(urls)


@app.route("/")
def home():
    return "<H2>HOLA MUNDO</H2>"

if __name__ == '__main__':
    app.run(port=port)
