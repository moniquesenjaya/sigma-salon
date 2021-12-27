from flask import Blueprint, render_template, flash, request
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


@views.route("/register-new", methods=["GET", "POST"])
def register_new():
    username = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        sex = request.form.get("sex")
        birthdate = request.form.get("birthdate")

        # Validations
        if len(username) < 4:
            flash("Username must be at least 4 characters", category="error")
        elif len(password) < 4:
            flash("Password must be at least 4 characters", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character", category="error")
        elif len(last_name) < 2:
            flash("Last name must be greater than 1 character", category="error")
        elif len(sex) < 1:
            flash("Sex must be at least 1 character", category="error")
        elif birthdate == "":
            flash("Enter a valid birthdate", category="error")
        else:
            # Add user to database
            # TODO: put register stuff here to the db
            flash("Account created!", category="success")
            return render_template("register-new.html", username=username)

    return render_template("register-new.html")
