from src.backend.db import get_db


def login_user(username: str, password: str):
    db = get_db()
    cursor = db.cursor()

    # Query for comparing password in db with the one entered in
    # query = "SELECT personId FROM person WHERE username=%s and password=%s;"
    query = "SELECT p.personId, c.custId, s.position FROM person as p LEFT JOIN customers as c ON c.personId = p.personId LEFT JOIN staffs as s ON s.personId = p.personId WHERE username=%s and password=%s;"

    cursor.execute(query, (username, password))

    res = cursor.fetchone()
    if res == None:
        return False

    person_id = res[0]
    cust_id = res[1]
    position = res[2]

    return (person_id, cust_id, position)
