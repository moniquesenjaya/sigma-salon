from flask import Flask, render_template
from decouple import config
from db import getDb

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    from src.frontend.views import views

    app.register_blueprint(views, url_prefix="/")

    return app