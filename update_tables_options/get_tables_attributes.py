import sqlite3
import os
from icecream import ic
import re

from code_tools import clear_code, split_code


sql_queries = {
    "get_table_id": """
        SELECT c.ID_tblCatalog
        FROM tblCatalogs c
        WHERE
            c.FK_tblCatalogs_tblDirectoryItems = (
                SELECT di.ID_tblDirectoryItem FROM tblDirectoryItems di WHERE di.name = 'Таблица'
                )
                AND c.code REGEXP ?; --'^4\.8-\d+-\d+-0-288'
    """,

    "get_attributes_table_id": """
        SELECT DISTINCT a.name
        FROM tblAttributes a
        WHERE a.FK_tblAttributes_tblQuotes IN (
            SELECT q.ID_tblQuote FROM tblQuotes q WHERE q.FK_tblQuotes_tblCatalogs = ?
        );
    """,

    "get_attributes_table_code": """
        SELECT
          DISTINCT a.name AS attribute
        FROM
          tblAttributes a 
        WHERE
          a.FK_tblAttributes_tblQuotes IN (
              SELECT
                q.ID_tblQuote
              FROM
                tblQuotes q 
              WHERE
                q.FK_tblQuotes_tblCatalogs = (
                    SELECT
                      c.ID_tblCatalog
                    FROM
                      tblCatalogs c 
                    WHERE
                      c.FK_tblCatalogs_tblDirectoryItems = (
                          SELECT
                            di.ID_tblDirectoryItem
                          FROM
                            tblDirectoryItems di 
                          WHERE
                            di.name = 'Таблица'
                        )
                      AND c.code REGEXP ?
                  )
            );    
    """,

    "get_value_attribute_name_table_id": """
        SELECT
          COUNT(DISTINCT a.value)
        FROM
          tblAttributes a
        WHERE
          a.name = ?
          AND a.FK_tblAttributes_tblQuotes IN (
              SELECT
                q.ID_tblQuote
              FROM
                tblQuotes q
              WHERE
                q.FK_tblQuotes_tblCatalogs = ?
            );    
    """,

}


def test_connections(db_name: str):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cur = conn.execute("select count(*) as count from tblCatalogs;")
    ic(cur.description)
    result = cur.fetchone()
    ic(result.keys())
    ic(tuple(result))

    # cur = conn.execute("select * from tblCatalogs;")
    # result = [tuple(row) for row in cur.fetchall()]
    # ic(len(result))

    # for row in cur.fetchall():
    #     ic(row.keys())
    #     ic(tuple(row))
    #     ic(row['code'], row['descriptions'])

    conn.close()


def build_re_pattern_full_table_code(short_table_code: str) -> str:
    """ Создает строку-паттерн для регулярного выражения поиска таблицы по короткому номеру. """
    # 4.8-288 -> r"^4\.8-\d+-\d+-0-288"
    if short_table_code:
        code_parts = split_code(clear_code(short_table_code))
        if len(code_parts) == 3:
            return fr"^{code_parts[0]}\.{code_parts[1]}-\d+-\d+-0-{code_parts[2]}"
    return ""


def get_table_attributes(db_name: str, table_short_code: str):
    def regex(expression, item):
        reg = re.compile(expression)
        return reg.search(item) is not None

    table_pattern = build_re_pattern_full_table_code(table_short_code)              # r"^4\.8-\d+-\d+-0-288"
    try:
        with sqlite3.connect(db_name, check_same_thread=False) as connection:
            connection.create_function("REGEXP", 2, regex)
            connection.row_factory = sqlite3.Row
            # --------------------------------------------------------------
            cur = connection.execute(sql_queries["get_table_id"], (table_pattern,))
            res = cur.fetchone() if cur else None
            if res:
                ic(res.keys(), res['ID_tblCatalog'])
                table_id = res['ID_tblCatalog']

            cur = connection.execute(sql_queries["get_attributes_table_code"], (table_pattern,))
            res = cur.fetchall() if cur else None
            if res:
                attributes = [row['attribute'] for row in res]
                ic(attributes)

                if len(attributes) > 0:
                    for attribute in attributes:
                        cur = connection.execute(sql_queries["get_value_attribute_name_table_id"], (attribute, table_id))
                        res = cur.fetchall() if cur else None
                        if res:

                            ic(attribute, tuple(res[0]))



    except (sqlite3.OperationalError, sqlite3.IntegrityError) as err:
        print('Ошибка при открытии БД:', err)


if __name__ == '__main__':

    data_path = r""
    db_path = r"F:\Kazak\GoogleDrive\Python_projects\DB"

    db_name = os.path.join(db_path, "quotes_test.sqlite3")
    ic(db_name)

    # test_connections(db_name)

    get_table_attributes(db_name, "  4.10-89 ")

