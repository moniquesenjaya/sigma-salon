from mysql.connector import connect
import mysql.connector
from decouple import config


# Connect to the database
# Double underscore means private. Means that it cannot be imported
__db = connect(
    host=config("HOST"),
    user=config("USER"),
    password=config("PASSWORD"),
    database=config("DATABASE"),
    port=config("PORT"),
)

# Simple logic that will reconnect if the connection is severed
def get_db():
    """Constantly checks if the application is connected with the database or not
    """
    if not __db.is_connected():
        __db.reconnect()
    return __db


# Returns MySQL errors for exceptions
def get_error():
    return mysql.connector.Error
