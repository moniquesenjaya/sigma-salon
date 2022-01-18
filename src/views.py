from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
import requests as r
from src.state import state

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", state=state)
