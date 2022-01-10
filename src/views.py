from flask import Blueprint, render_template, flash, request

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return render_template("index.html", number=100)


@views.route("/register", methods=["GET", "POST"])
def register():
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
        elif sex.upper() not in ["M", "F"]:
            flash("Sex must be either M or F", category="error")
        elif birthdate == "":
            flash("Enter a valid birthdate", category="error")
        else:
            # Add user to database
            # TODO: put register stuff here to the db
            flash("Account created!", category="success")
            return render_template("register.html", username=username)

    return render_template("register.html")
