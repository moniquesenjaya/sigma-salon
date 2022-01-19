from flask import Blueprint, render_template, flash, request, redirect, url_for
from datetime import datetime, timedelta
import src.backend.api.tableapi as tableapi
import src.backend.api.userapi as userapi
from src.state import state
import json


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
    if request.method == "POST" and state["logged_in"]:
        seat_limit = request.form.get("seatLimit")
        branch_name = request.form.get("branchName")
        city = request.form.get("city")

        if not 2 < len(branch_name) < 40:
            flash("Branch name must be between 2 and 40 characters", category="error")
        elif not 2 < len(city) < 20:
            flash("City must be between 2 and 20 characters", category="error")
        else:
            # Add branch to database
            tableapi.register_branch(int(seat_limit), branch_name, city)

            flash("Branch created!", category="success")
            return render_template("admin/manage_branch.html", state=state)

    return render_template("admin/manage_branch.html", state=state)


@views.route("/admin/manage_salary", methods=["GET", "POST"])
def manage_salary():
    if request.method == "POST" and state["logged_in"]:
        staff_id = request.form.get("staffId")
        amount = request.form.get("amount")

        #validate staffid
        if not userapi.check_staffId(staff_id):
            flash("Staff ID not found", category="error")
        elif not 2 < len(amount) < 11:
            flash("Amount's number of digits must be between 2 and 11 characters", category="error")
        else:
            tableapi.register_salary(int(staff_id), int(amount))

            flash("Salary updated!", category="success")
            return render_template("admin/manage_salary.html", state=state)

    return render_template("admin/manage_salary.html", state=state)


@views.route("/admin/manage_service", methods=["GET", "POST"])
def manage_service():
    if request.method == "POST" and state["logged_in"]:
        service_name = request.form.get("serviceName")
        time = request.form.get("time")

        if not 2 < len(service_name) < 30:
            flash("Service name must be between 2 and 30 characters", category="error")
        else:
            tableapi.register_service(service_name, int(time))

            flash("Service created!", category="success")
            return render_template("admin/manage_service.html", state=state)

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

        return render_template("admin/view_appointments.html", state=state, appointments=result)

    return render_template("admin/view_appointments.html", state=state)


# Staff routes
@views.route("/staff/manage_appointments", methods=["GET", "POST"])
def manage_appointments():
    if request.method == "POST" and state["logged_in"]:
        appointment_id = request.form.get("appointmentId")

        if not tableapi.check_appointment(appointment_id):
            flash("AppointmentId doesn't exist!", category="error")
        else:
            # Mark appointment as done in database
            tableapi.update_appointment(appointment_id)

            flash("Appointment updated!", category="success")
            return render_template("staff/manage_appointments.html", state=state)

    if state["logged_in"]:
        result = tableapi.get_appointments(state["staff_id"])
        return render_template("staff/manage_appointments.html", state=state, appointments=result)

    return render_template("staff/manage_appointments.html", state=state)


# Customer routes
@views.route("/customer/book_appointments", methods=["GET", "POST"])
def book_appointments():
    if request.method == "POST" and state["logged_in"]:
        branch = request.form.get("branchName")[2:-3]
        service = request.form.get("serviceName")[2:-3]

        return redirect(url_for("views.book_appointments_staff", branch=branch, service=service, state=state))

    if state["logged_in"]:
        branch_name = tableapi.get_branch_name()
        service_name = tableapi.get_service_name()

        return render_template("customer/book_appointments.html", state=state, branches=branch_name, services=service_name)

    return render_template("customer/book_appointments.html", state=state)


@views.route("/customer/book_appointments_staff/<branch>/<service>", methods=["GET", "POST"])
def book_appointments_staff(branch:str, service:str):
    if request.method == "POST" and state["logged_in"]:
        staff_id = request.form.get("staffId")

        return redirect(url_for("views.book_appointments_time", branch=branch, service=service, staffId=int(staff_id)))

    if state["logged_in"]:
        staff = tableapi.get_available_staff(branch, service)

        return render_template("customer/book_appointments_staff.html", state=state, branch=branch, service=service, staff=staff)

    return render_template("customer/book_appointments_staff.html", state=state)


@views.route("/customer/book_appointments_time/<branch>/<service>/<staffId>", methods=["GET", "POST"])
def book_appointments_time(branch:str, service:str, staffId:int):
    if request.method == "POST" and state["logged_in"]:
        date = request.form.get("date")
        time = request.form.get("time")
        starttime = date + " " + time
        time = datetime.strptime(time, "%H:%M:%S")
        endtime = time + timedelta(minutes=float(tableapi.get_service_time(service)[0]))
        endtime = date + " " + str(endtime)[-9:]

        if datetime.strptime(date, "%Y-%m-%d") < datetime.now():
            flash("Date cannot be less than today", category="error")
        else:
            tableapi.register_appointment(state["cust_id"], staffId, service, date, starttime, endtime)
            flash("Appointment registered!", category="success")

            return render_template("/customer/book_appointments_time.html", branch=branch, service=service, staffId=staffId, starttime=starttime, endtime=endtime, state=state)

    if state["logged_in"]:
        appointments = tableapi.get_staff_appointment(staffId)

        return render_template("customer/book_appointments_time.html", branch=branch, service=service, staffId=staffId, appointments=appointments, state=state)
    return render_template("customer/book_appointments_time.html", state=state)
