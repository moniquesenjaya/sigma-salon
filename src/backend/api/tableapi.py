from src.backend.db import get_db, get_error
import datetime


def get_all_tables():
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


def get_appointments(staffId=None):
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


def get_query(query):
    db = get_db()
    cursor = db.cursor()

    try:
        # Free query, except for certain queries
        cursor.execute(query)
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
