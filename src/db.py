from mysql.connector import connect
from decouple import config
# Connect to the database
# Double underscore means private. Means that it cannot be imported
__db = connect(
  host=config('HOST'),
  user=config('USER'),
  password=config('PASSWORD'),
  database=config('DATABASE'),
  port=config('PORT')
)

# Simple logic that will reconnect if the connection is severed
def getDb():
  if not __db.is_connected():
    __db.reconnect()
  return __db