import sqlite3
import os
from icecream import ic
import re

from db.sql_queries import create_table, insert_query
from excel_tools import get_data_from_excel
from files_tolls import output_message_exit


def create_db(path_db: str):
    try:
        with sqlite3.connect(path_db) as connection:
            connection.execute(create_table["create_raw_parse"])
            ic(connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
            for field in connection.execute("""PRAGMA table_info(tblRawParsers);"""):
                ic(field)
    except (sqlite3.OperationalError, sqlite3.IntegrityError) as err:
        connection.rollback()
        print('Ошибка при создании таблиц:', err)


#
# def insert_db(path_db: str, src_data: tuple):
#     try:
#         with sqlite3.connect(path_db) as connection:
#             cursor = connection.execute(insert_querys["insert_raw_parsers"], src_data)
#             ic(cursor.lastrowid)
#             connection.commit()
#     except (sqlite3.OperationalError, sqlite3.IntegrityError) as err:
#         connection.rollback()
#         print('ошибка вставки:', err)
#
#
def insert_multiple_db(path_db: str, data_set: list = None):
    try:
        with sqlite3.connect(path_db) as connection:
            cursor = connection.executemany(insert_query["insert_raw_parsers"], data_set)
            ic(cursor.rowcount)
            connection.commit()
    except (sqlite3.OperationalError, sqlite3.IntegrityError) as err:
        connection.rollback()
        print('ошибка вставки данных в БД:', err)




def read_data(src_data_path: str, db_file_name: str)-> bool:
    xlsx_mask = re.compile(r"[^~].*[\d+]((\d+-){4}).*\.xlsx")
    data_files = [os.path.join(src_data_path, file)
                  for file in os.listdir(src_data_path)
                  if xlsx_mask.match(file)]
    if data_files:
        ic(data_files)
        create_db(db_file_name)
        for file in data_files:
            data_set = get_data_from_excel(file)
            insert_multiple_db(db_file_name, data_set)
            # ic(data_set)
        return True
    else:
        output_message_exit(f"Фалы с данными не найдены", f"{src_data_path!r}")
    return False




if __name__ == "__main__":
    src_data_path = r'F:\Kazak\GoogleDrive\NIAC\PSM'
    db_file_name = r'..\output\PSM.sqlite3'
    read_data(src_data_path, db_file_name)