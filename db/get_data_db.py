import sqlite3

from db.sql_queries import select_query
from files_tolls import output_message


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
    """
    Получает данные из БД по запросу, вставляет заголовки столбцов
    :param db_file_name: БД
    :param query: запрос
    :return: кортеж значений и заголовок
    """

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


def get_statistics_data(db_file_name: str) -> tuple:
    """
        Формирует список уникальных значений колонки 'criteria', сортирует его.
        Создает запрос к БД для подсчета этих значений.
        Получает статистику по колонке 'criteria' из БД.

    """
    unique_criteria = get_data_db(db_file_name, select_query["select_unic_criteria"])
    unique_criteria = list(map(lambda x: x[0], unique_criteria))
    unique_criteria.sort(key=lambda x: (x[0], int(x[1:])))
    if unique_criteria:
        rising_line = ", ".join(
            map(lambda x: f"SUM(CASE WHEN criteria = '{x}' THEN 1 ELSE 0 END) AS {x}", unique_criteria)
        )
        query = f"""
            SELECT file_name,
                COUNT(DISTINCT ID_tblRawParser) AS 'всего',
                {rising_line}
            FROM tblRawParsers
            GROUP BY file_name;
        """
        return get_db_data_with_header(db_file_name, query)

    return tuple()


if __name__ == "__main__":
    db_file_name = r'..\output\PSM.sqlite3'
    x = get_statistics_data(db_file_name)
    print(x)
