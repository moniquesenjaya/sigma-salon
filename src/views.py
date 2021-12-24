from flask import Blueprint, render_template, flash
from src.forms import RegisterForm

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return render_template("index.html", number=100)


@views.route("/register", methods=["GET", "POST"])
def register():
    username = None
    password = None
    first_name = None
    middle_name = None
    last_name = None
    sex = None
    birthdate = None
    password_check = None
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ""
        first_name = form.first_name.data
        form.first_name.data = ""
        middle_name = form.middle_name.data
        form.middle_name.data = ""
        last_name = form.last_name.data
        form.last_name.data = ""
        sex = form.sex.data
        form.sex.data = ""
        birthdate = form.birthdate.data
        form.birthdate.data = ""
        password = form.password.data
        form.password.data = ""
        password_check = form.password_check.data
        form.password_check.data = ""
        # put register stuff here to the db
        flash("Registered successfully!")
    return render_template(
        "register.html",
        username=username,
        password=password,
        password_check=password_check,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        sex=sex,
        birthdate=birthdate,
        form=form,
    )
