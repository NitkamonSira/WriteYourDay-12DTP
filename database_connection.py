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
    """check that the user data that was entry match with the data in the database or not

    Args:
        require (str): the column name of database that need to be check with
        check (str): the column name that use for filter the data to match the need
        input_taken (Any): the input that need to be check that it match or exist in the database

    Returns:
        bool: False for don't exist in database and True for match or have
    """
    query = f"SELECT {require} FROM Test WHERE {check} = ?;"
    result = get_data_from_database(query,(input_taken,))
    if len(result) == 0:
        return False
    else:
        return True