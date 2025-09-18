import sqlite3

DATABASE = "diary.db"


def get_data_from_database(query, params=None):
    """_summary_

    Args:
        query (str): query that use to get the data from database
        params (tuple, optional): Variable that need to pass in with the query.
        Defaults to None.

    Returns:
        list: list of the data that got from database
    """
    with sqlite3.connect(DATABASE) as db:  # connected with database
        cursor = db.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        results = cursor.fetchall()
    return results


def update_data(query, params=None):
    """insert data into database

    Args:
        query (str): query use to insert/update/delete data
        params (tuple, optional): Variable that need to pass in with the query.
        Defaults to None.

    Returns:
        int: id of the row that just inserted
    """
    with sqlite3.connect(DATABASE) as db:  # connect with database
        cursor = db.cursor()
        if params is None:
            cursor.execute(query)
            last_id = cursor.lastrowid
        else:
            cursor.execute(query, params)
            last_id = cursor.lastrowid
        db.commit()
    return last_id


def check_user_data(require, check, input_taken):
    """check that the user data that was entry match with the data in the database or not

    Args:
        require (str): the column name of database that need to be check with
        check (str): the column name that use for filter the data to match the need
        input_taken (Any): the input that need to be check that it match
                           or exist in the database

    Returns:
        bool: False for don't exist in database and True for match or have
    """
    query = f"SELECT {require} FROM User WHERE {check} = ?;"
    result = get_data_from_database(query, (input_taken,))

    # check that data exist in database or not
    # result should be blank list if data doesn't exist
    if len(result) == 0:
        return False
    else:
        return True
