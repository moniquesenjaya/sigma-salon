from flask import Blueprint, render_template, redirect, url_for, flash, request
import json
import src.backend.api.tableapi as tableapi
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


@views.route("/admin/manage_staff", methods=["GET", "POST"])
def manage_staff():
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
