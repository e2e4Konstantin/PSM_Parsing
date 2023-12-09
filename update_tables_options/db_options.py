from icecream import ic

from config import dbTolls
from files_tolls import output_message

from update_tables_options.db_tools import (
    get_table_id_number_quotes, get_distinct_options_for_table, get_values_options_for_table
)




def get_db_options_for_table(db: dbTolls, table_short_name: str) -> dict[str: tuple[str, ...]] | None:
    """ Для таблицы с коротким шифром создает словарь уникальных параметров и уникальных значений к ним,
        если эти значения менялись у расценок которые входят в таблицу.
    """

    table_id, number_quotes = get_table_id_number_quotes(db, table_short_name)
    if number_quotes is None:
        return None

    options = get_distinct_options_for_table(db, table_id)
    if options is None:
        output_message(f"в таблице {table_short_name} для всех {number_quotes} расценок",
                       f"нет ни одного параметра")
        return None
    variable_options = {}
    for option in options:
        options_values = get_values_options_for_table(db, option, table_id)
        if options_values:
            variable_options[option] = option
            ic(option, variable_options[option])
    return variable_options


if __name__ == '__main__':
    import os

    db_path = r"F:\Kazak\GoogleDrive\Python_projects\DB"
    db_name = os.path.join(db_path, "quotes_test.sqlite3")
    ic(db_name)

    table = '4.8-176'
    with dbTolls(db_name) as dbt:
        uo = get_db_options_for_table(dbt, table)
