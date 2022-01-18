from flask import Blueprint, render_template, redirect, url_for, flash, request
import json
import src.backend.api.tableapi as tableapi
import src.backend.api.userapi as userapi
import requests as r
from src.state import state

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", state=state)


# Admin routes
@views.route("/admin/all_tables", methods=["GET"])
def all_tables():
    if state["logged_in"]:
        result = tableapi.get_all_tables()

        return render_template("admin/all_tables.html", state=state, tables=result)

    return render_template("admin/all_tables.html", state=state)


@views.route("/admin/free_query", methods=["GET", "POST"])
def free_query():
    if request.method == "POST" and state["logged_in"]:
        query = request.form.get("query")
        result = tableapi.get_query(query)

        return render_template("admin/free_query.html", state=state, result=json.dumps(result, default=str)) # set default to str in order to handle date objects

    return render_template("admin/free_query.html", state=state, query=None)


@views.route("/admin/manage_branch", methods=["GET", "POST"])
def manage_branch():
    return render_template("admin/manage_branch.html", state=state)


@views.route("/admin/manage_salary", methods=["GET", "POST"])
def manage_salary():
    return render_template("admin/manage_salary.html", state=state)


@views.route("/admin/manage_service", methods=["GET", "POST"])
def manage_service():
    return render_template("admin/manage_service.html", state=state)


@views.route("/admin/manage_staff", methods=["GET", "POST"])
def manage_staff():
    if request.method == "POST" and state["logged_in"]:
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        sex = request.form.get("sex")
        birthdate = request.form.get("birthdate")
        position = request.form.get("position")
        branch_id = request.form.get("branchId")
        service_id = request.form.get("serviceId")

        # Form validations
        if not 4 < len(username) < 30:
            flash("Username must be between 4 and 30 characters", category="error")
        elif not userapi.check_username(username):
            # Username not unique
            flash("Username has been taken!", category="error")
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
        elif position.capitalize() not in ["Admin", "Staff"]:
            flash("Position must be either Admin or Staff", category="error")
        elif not tableapi.check_branch(int(branch_id)):
            # BranchId doesn't exist
            flash("BranchId doesn't exist!", category="error")
        elif not tableapi.check_service(int(service_id)):
            # ServiceId doesn't exist
            flash("ServiceId doesn't exist!", category="error")
        else:
            # Add staff to database
            userapi.register_staff(username, password, first_name, last_name, sex, birthdate, position.replace('\"', '\''), int(branch_id), int(service_id))

            flash("Account created!", category="success")
            return render_template("admin/manage_staff.html", state=state)

    return render_template("admin/manage_staff.html", state=state)


@views.route("/admin/view_appointments", methods=["GET"])
def view_appointments():
    if state["logged_in"]:
        result = tableapi.get_appointments()
        print(result)

        return render_template("admin/view_appointments.html", state=state, appointments=result)
    return render_template("admin/view_appointments.html", state=state)


# Staff routes
@views.route("/staff/manage_appointments", methods=["GET", "POST"])
def manage_appointments():
    return render_template("staff/manage_appointments.html", state=state)


# Customer routes
@views.route("/customer/book_appointments", methods=["GET", "POST"])
def book_appointments():
    return render_template("customer/book_appointments.html", state=state)
