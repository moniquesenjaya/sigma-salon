from flask import Blueprint, render_template, flash
from src.frontend.forms import RegisterForm

views = Blueprint("views", __name__, template_folder="templates", static_folder="static")


@views.route("/")
def index():
    return render_template("index.html", number=100)

@views.route("/register", methods=['GET', 'POST'])
def register():
    username = None
    password = None
    password_check = None
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ''
        password = form.password.data
        form.password.data = ''
        password_check = form.password_check.data
        form.password_check.data = ''
        flash("Registered successfully!")
    return render_template("register.html",
                            username = username,
                            password = password,
                            password_check = password_check,
                            form = form)
