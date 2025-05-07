import sqlite3

DATABASE = "diary.db"


def access_database(query, params=None):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        results = cursor.fetchall()

def check_user_data(require, check, input_taken):
    query = f"SELECT {require} FROM User WHERE {check} = ?;"
    result = access_database(query,(input_taken,))
    if len(result) == 0:
        return False