from config import dbTolls
from files_tolls import output_message
from update_tables_options.db_tools import (
    get_table_id, get_table_number_quotes, get_distinct_attributes_for_table, get_values_attribute_for_table
)


def get_db_attributes_for_table(db: dbTolls, table_short_name: str) -> dict[str: tuple[str, ...]] | None:
    """ Для таблицы с коротким шифром создает словарь уникальных атрибутов и уникальных значений к ним,
        если эти значения менялись у расценок которые входят в таблицу.
    """
    table_id = get_table_id(db, table_short_name)
    if table_id is None:
        output_message(f"в БД не найдена таблица:", f"данные: {table_short_name}")
        return None
    quotes_number = get_table_number_quotes(db, table_id)
    if quotes_number is None:
        output_message(f"не удалось подсчитать количество расценок", f"в таблице с id: {table_id}")
        return None
    attributes = get_distinct_attributes_for_table(db, table_id)
    if attributes is None:
        output_message(f"в таблице {table_short_name} для всех {quotes_number} расценок",
                       f"нет ни одного атрибута")
        return None
    variable_attributes = {}
    for attribute in attributes:
        attribute_values = get_values_attribute_for_table(db, attribute, table_id)
        if attribute_values and (len(attribute_values) < quotes_number
                                 or len(set(attribute_values)) > 1):
            variable_attributes[attribute] = tuple(set(attribute_values))
            # ic(attribute, variable_attributes[attribute])
    return variable_attributes


if __name__ == '__main__':
    import os
    from icecream import ic

    db_path = r"F:\Kazak\GoogleDrive\Python_projects\DB"
    db_name = os.path.join(db_path, "quotes_test.sqlite3")
    ic(db_name)

    table = (13, '2', '4.8-243')
    with dbTolls(db_name) as dbt:
        ua = get_db_attributes_for_table(dbt, table[2])
        ic(ua)
