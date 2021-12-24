from flask import Flask, render_template
from decouple import config

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    from src.views import views

    app.register_blueprint(views, url_prefix="/")

    return app