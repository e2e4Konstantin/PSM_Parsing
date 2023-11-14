import sqlite3

from db.sql_queries import select_query


# def get_data_db(db_file_name: str) -> tuple:
#     try:
#         with sqlite3.connect(db_file_name) as connection:
#             result = [row for row in connection.execute(select_query["select_all_raw_parsers"])]
#         if result:
#             return tuple(result)
#     except (sqlite3.OperationalError, sqlite3.IntegrityError) as err:
#         connection.rollback()
#         print('получение данных из БД:', err)
#     return tuple()

def get_data_db(db_file_name: str, query: str) -> tuple:
    try:
        with sqlite3.connect(db_file_name) as connection:
            result = [row for row in connection.execute(query)]
        if result:
            return tuple(result)
    except (sqlite3.OperationalError, sqlite3.IntegrityError) as err:
        connection.rollback()
        print('получение данных из БД:', err)
    return tuple()


def get_db_data_with_header(db_file_name: str, query: str) -> tuple:
    try:
        with sqlite3.connect(db_file_name) as connection:
            cursor = connection.execute(query)
            names = list(map(lambda x: x[0], cursor.description))
            result = [row for row in connection.execute(query)]
            result.insert(0, tuple(names))
        if result:
            return tuple(result)
    except (sqlite3.OperationalError, sqlite3.IntegrityError) as err:
        connection.rollback()
        print('получение данных из БД:', err)
    return tuple()