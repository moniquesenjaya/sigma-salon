from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
import src.backend.api.userapi as userapi
from src.state import state
import time

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Form validations
        if len(username) <= 0:
            flash("Enter a valid username!", category="error")
        elif len(password) <= 0:
            flash("Enter a valid password!", category="error")

        # Login validation
        result = userapi.login_user(username, password)

        if not result:
            flash("Invalid credentials! Try again!", category="error")
            return render_template("login.html", state=state)
        else:
            print(result)
            state["username"] = username
            state["person_id"] = result[0]
            state["cust_id"] = result[1]
            state["position"] = result[2]
            state["logged_in"] = True
            return redirect(url_for("views.index"))

    return render_template("login.html", state=state)


@auth.route("/logout", methods=["GET"])
def logout():
    state["username"] = ""
    state["person_id"] = None
    state["cust_id"] = None
    state["logged_in"] = False
    state["position"] = None
    return redirect(url_for("views.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        sex = request.form.get("sex")
        birthdate = request.form.get("birthdate")

        # Form validations
        if not 4 < len(username) < 30:
            flash("Username must be between 4 and 30 characters", category="error")
        elif not 4 < len(password) < 100:
            flash("Password must be at least 4 characters", category="error")
        elif not 2 < len(first_name) < 30:
            flash("First name must be between 2 and 30 characters", category="error")
        elif not 2 < len(last_name) < 30:
            flash("Last name must be between 2 and 30 characters", category="error")
        elif sex.lower() not in ["male", "female"]:
            flash("Sex must be either male or female", category="error")
        elif birthdate == "":
            flash("Enter a valid birthdate", category="error")
        else:
            # Add user to database
            # TODO: put register stuff here to the db
            flash("Account created!", category="success")
            return render_template("register.html", state=state)

    return render_template("register.html", state=state)
