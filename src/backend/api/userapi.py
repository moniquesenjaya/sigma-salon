from src.backend.db import get_db
from typing import Tuple


def login_user(username: str, password: str) -> Tuple:
    db = get_db()
    cursor = db.cursor()

    # Query for comparing password in db with the one entered in
    query = "SELECT p.personId, c.custId, s.position FROM person as p LEFT JOIN customers as c ON c.personId = p.personId LEFT JOIN staffs as s ON s.personId = p.personId WHERE username=%s and password=%s;"

    cursor.execute(query, (username, password))

    res = cursor.fetchone()
    if res == None:
        return False

    person_id = res[0]
    cust_id = res[1]
    position = res[2]

    return (person_id, cust_id, position)


def register_user(username:str, password:str, firstName:str, lastName:str, sex:str, dateOfBirth:str) -> bool:
    db = get_db()
    cursor = db.cursor()

    # Queries for inserting new user to the database
    query1 = "INSERT INTO person (username, password, firstName, lastName, sex, dateOfBirth) VALUES (%s, %s, %s, %s, %s, %s);"
    query2 = "SELECT personId FROM person WHERE username=%s;"

    cursor.execute(query1, (username, password, firstName, lastName, sex, dateOfBirth))
    db.commit()

    cursor.execute(query2, (username, ))
    person_id = int(str(cursor.fetchone()).strip('(),')) # Converting from tuple to int
    query3 = f"INSERT INTO customers(personId, membership) VALUES ({person_id}, 0);"
    cursor.execute(query3)
    db.commit()

    return True


def check_username(username:str) -> bool:
    db = get_db()
    cursor = db.cursor(buffered=True)

    # Query for checking all usernames from person table
    query = "SELECT username FROM person;"
    cursor.execute(query)

    res = cursor.fetchall()

    # If username is already registered, return True
    if username in str(res):
        return False
    else:
        return True
