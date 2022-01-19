from typing import List, Tuple
from src.backend.db import get_db, get_error
import datetime


def get_all_tables() -> List:
    results = []

    db = get_db()
    cursor = db.cursor()

    try:
        # Query all the tables and append the result in to results list
        # person table
        cursor.execute("SELECT * FROM person;")
        results.append(cursor.fetchall())

        # customer data
        cursor.execute("SELECT p.personId, p.username, p.firstName, p.lastName, p.sex, p.dateOfBirth, c.membership FROM person AS p JOIN customers AS c ON c.personId = p.personId;")
        results.append(cursor.fetchall())

        # staff data
        cursor.execute("SELECT p.personId, s.staffId, p.username, p.firstName, p.lastName, p.sex, p.dateOfBirth, s.position, b.branchName, sr.serviceName FROM person AS p INNER JOIN staffs AS s ON s.personId = p.personId INNER JOIN branch AS b ON b.branchId = s.branchId INNER JOIN services AS sr ON sr.serviceId = s.serviceId;")
        results.append(cursor.fetchall())

        # branch table
        cursor.execute("SELECT * FROM branch;")
        results.append(cursor.fetchall())

        # services table
        cursor.execute("SELECT * FROM services;")
        results.append(cursor.fetchall())

        # appointments data
        cursor.execute("SELECT a.appointmentId, a.date, a.startTime, a.endTime, a.staffId, a.custId, sr.serviceName, a.progress FROM appointments as a INNER JOIN services AS sr ON sr.serviceId = a.serviceId;")
        results.append(cursor.fetchall())

        # salary data
        cursor.execute("SELECT sa.salaryId, sa.date, sa.amount, p.personId, s.staffId, p.username, p.firstName, p.lastName, p.sex, p.dateOfBirth, s.position, b.branchName, sr.serviceName FROM salary AS sa INNER JOIN staffs AS s ON s.staffId = sa.staffId INNER JOIN person AS p ON p.personId = s.personId INNER JOIN branch AS b  ON b.branchId = s.branchId INNER JOIN services AS sr ON sr.serviceId = s.serviceId;")
        results.append(cursor.fetchall())
    except get_error() as error:
        print(error)
        pass

    return results


def get_appointments(staffId=None) -> Tuple:
    db = get_db()
    cursor = db.cursor()

    try:
        if staffId:
            # Query appointsment, service, and person table to get appointments data of a specific staffId
            query = "SELECT a.appointmentId, a.date, a.startTime, a.endTime, sr.serviceName, p.firstName, p.lastName FROM appointments as a INNER JOIN staffs AS s ON s.staffId = a.staffId INNER JOIN services AS sr ON sr.serviceId = a.serviceId INNER JOIN customers AS c ON c.custId = a.custId INNER JOIN person AS p ON p.personId = c.personId WHERE a.staffId = %s AND a.progress = 'Not Done';"
            cursor.execute(query, (staffId, ))
        else:
            # Query appointments table and service table to get all appointments data
            cursor.execute("SELECT a.appointmentId, a.date, a.startTime, a.endTime, a.staffId, a.custId, sr.serviceName, a.progress FROM appointments as a INNER JOIN services AS sr ON sr.serviceId = a.serviceId;")
    except get_error() as error:
        print(error)
        pass

    return cursor.fetchall()


def get_query(query) -> Tuple:
    db = get_db()
    cursor = db.cursor()

    try:
        # Free query
        cursor.execute(query)
    except get_error() as error:
        return error

    return cursor.fetchall()


def get_branch_name() -> Tuple:
    db = get_db()
    cursor = db.cursor()

    try:
        # Query for getting branch names from branch table
        cursor.execute("SELECT branchName from branch;")
    except get_error() as error:
        return error

    return cursor.fetchall()


def get_service_name() -> Tuple:
    db = get_db()
    cursor = db.cursor()

    try:
        # Query for getting service names from services table
        cursor.execute("SELECT serviceName from services;")
    except get_error() as error:
        return error

    return cursor.fetchall()


def get_service_time(serviceName:str):
    db = get_db()
    cursor = db.cursor()

    try:
        # Query for getting time for a specific service
        query = "SELECT time FROM services WHERE serviceName=%s;"
        cursor.execute(query, (serviceName, ))
    except get_error() as error:
        return error

    return cursor.fetchone()


def get_available_staff(branchName:str, serviceName:str) -> Tuple:
    db = get_db()
    cursor = db.cursor()

    try:
        # Query for getting all available staff depending on branch and service name
        query = "SELECT s.staffId, p.firstName, p.lastName, p.sex FROM person AS p INNER JOIN staffs AS s ON s.personId = p.personId  INNER JOIN branch AS b  ON b.branchId = s.branchId  INNER JOIN services AS sr ON sr.serviceId=s.serviceId WHERE b.branchName=%s AND sr.serviceName=%s;"
        cursor.execute(query, (branchName, serviceName))
    except get_error() as error:
        return error

    return cursor.fetchall()


def get_staff_appointment(staffId:int) -> Tuple:
    db = get_db()
    cursor = db.cursor()

    try:
        # Query for getting appointments depending on staff id
        query = "SELECT a.date, a.startTime, a.endTime FROM appointments as a INNER JOIN staffs AS s ON s.staffId=a.staffId WHERE a.staffId=%s AND a.progress='Not Done';"
        cursor.execute(query, (staffId, ))
    except get_error() as error:
        return error

    return cursor.fetchall()


def register_branch(seatLimit:int, branchName:str, city:str) -> bool:
    db = get_db()
    cursor = db.cursor()

    # Query for inserting new branch to the database
    query = "INSERT INTO branch (seatLimit, branchName, city) VALUES (%s, %s, %s);"
    cursor.execute(query, (seatLimit, branchName, city))
    db.commit()

    return True


def register_salary(staffId:int, amount:int) -> bool:
    db = get_db()
    cursor = db.cursor()

    # Query for inserting new branch to the database
    query = "INSERT INTO salary(date, amount,staffId) VALUES (%s, %s, %s);"
    date = datetime.date.today().isoformat()
    cursor.execute(query, (date, amount, staffId))
    db.commit()

    return True


def register_service(service_name:str, time:int) -> bool:
    db = get_db()
    cursor = db.cursor()

    # Query for inserting new branch to the database
    query = "INSERT INTO services (serviceName,time) VALUES (%s, %s);"
    cursor.execute(query, (service_name, time))
    db.commit()

    return True


def register_appointment(custId:int, staffId:int, serviceName:str, date:str, startTime:str, endTime:str):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(f"SELECT serviceId FROM services WHERE serviceName='{serviceName}'")
        serviceId = cursor.fetchone()[0]

        # Query for inserting new appointment
        query = "INSERT INTO appointments (custId, staffId, serviceId , date, startTime, endTime, progress) VALUES (%s, %s, %s, %s, %s, %s, 'Not Done');"
        cursor.execute(query, (custId, staffId, serviceId, date, startTime, endTime))
        db.commit()
    except get_error() as error:
        print(error)

    return True


def update_appointment(appointmentId:int) -> bool:
    db = get_db()
    cursor = db.cursor()

    # Query for updating appointment
    query = "UPDATE appointments SET progress = 'Done' WHERE appointmentId = %s;"
    cursor.execute(query, (appointmentId, ))
    db.commit()

    return True


def check_branch(branchId:int) -> bool:
    db = get_db()
    cursor = db.cursor(buffered=True)

    # Query for checking all branchId from branch table
    query = f"SELECT branchId FROM branch WHERE branchId={branchId};"
    cursor.execute(query)

    res = cursor.fetchone()

    if res:
        return True
    else:
        return False


def check_service(serviceId:int) -> bool:
    db = get_db()
    cursor = db.cursor(buffered=True)

    # Query for checking all serviceId from services table
    query = f"SELECT serviceId FROM services WHERE serviceId={serviceId};"
    cursor.execute(query)

    res = cursor.fetchone()

    if res:
        return True
    else:
        return False


def check_appointment(appointmentId:int) -> bool:
    db = get_db()
    cursor = db.cursor(buffered=True)

    # Query for checking all serviceId from services table
    query = f"SELECT appointmentId FROM appointments WHERE appointmentId={appointmentId};"
    cursor.execute(query)

    res = cursor.fetchone()

    if res:
        return True
    else:
        return False


def check_time(staffId:int, date:str, dateTime:str):
    db = get_db()
    cursor = db.cursor(buffered=True)

    # Query for checking if an appointment can be made for a certain staff at a certain time and date
    query = "SELECT appointmentId FROM appointments WHERE staffId=%s AND date=%s AND endtime < %s;"
    cursor.execute(query, (staffId, date, dateTime))

    res = cursor.fetchone()

    # If appointment can be made, return True
    if res:
        return False
    else:
        return True
