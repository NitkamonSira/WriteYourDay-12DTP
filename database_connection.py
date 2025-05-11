import sqlite3

DATABASE = "commit_test.db"


def get_data_from_database(query, params=None):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        results = cursor.fetchall()
    return results


def insert_data(query, params=None):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        db.commit()


def check_user_data(require, check, input_taken):
    query = f"SELECT {require} FROM User WHERE {check} = ?;"
    result = get_data_from_database(query,(input_taken,))
    if len(result) == 0:
        return False