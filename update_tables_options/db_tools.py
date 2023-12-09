from config import dbTolls
from update_tables_options.sql_attributes_options_queries import sql_queries
from code_tools import clear_code, split_code
from files_tolls import output_message


def build_re_pattern_full_table_code(short_table_code: str) -> str:
    """ Создает строку-паттерн для регулярного выражения поиска таблицы по короткому номеру. """
    # 4.8-288 -> r"^4\.8-\d+-\d+-0-288"
    if short_table_code:
        code_parts = split_code(clear_code(short_table_code))
        if len(code_parts) == 3:
            return fr"^{code_parts[0]}\.{code_parts[1]}-\d+-\d+-0-{code_parts[2]}"
    return ""


def get_table_id(db: dbTolls, table_short_name: str) -> int | None:
    """ По короткому коду получает id Таблицы.    """
    # создать паттерн для поиска таблицы в БД по полному шифру
    table_pattern = build_re_pattern_full_table_code(table_short_name)  # r"^4\.8-\d+-\d+-0-288"
    # получить id таблицы по паттерну
    cursor = db.go_execute(sql_queries["get_table_id"], (table_pattern,))
    result = cursor.fetchone() if cursor else None
    return result['ID_tblCatalog'] if result else None


def get_table_number_quotes(db: dbTolls, table_id: int) -> int | None:
    """ Считает количество расценок в таблице. """
    cursor = db.go_execute(sql_queries["count_number_table_quotes_by_id"], (table_id,))
    result = cursor.fetchone() if cursor else None
    return result['number'] if result else None


def get_table_id_number_quotes(db: dbTolls, table_short_name: str) -> tuple[int, int] | None:
    """ Возвращает id таблицы и количество расценок в таблице. """
    table_id = get_table_id(db, table_short_name)
    if table_id is None:
        output_message(f"в БД не найдена таблица:", f"данные: {table_short_name}")
        return None
    quotes_number = get_table_number_quotes(db, table_id)
    if quotes_number is None:
        output_message(f"не удалось подсчитать количество расценок", f"в таблице с id: {table_id}")
        return None
    return table_id, quotes_number


def get_distinct_attributes_for_table(db: dbTolls, table_id: int) -> tuple[str, ...] | None:
    """ Получает кортеж уникальных атрибутов для всех расценок из таблицы """
    cursor = db.go_execute(sql_queries["get_attributes_table_id"], (table_id,))
    result = cursor.fetchall() if cursor else None
    return tuple([row['attribute'] for row in result]) if result else None


def get_values_attribute_for_table(db: dbTolls, attribute_name: str, table_id: int) -> tuple[str, ...] | None:
    """ Получить все значения атрибута для всех расценок в таблице """
    cursor = db.go_execute(sql_queries["get_values_attribute_name_table_id"], (attribute_name, table_id))
    result = cursor.fetchall() if cursor else None
    return tuple([row['value'] for row in result]) if result else None


# --- > Options -------------------------------------------------------------------------

def get_distinct_options_for_table(db: dbTolls, table_id: int) -> tuple[str, ...] | None:
    """ Получает кортеж уникальных Параметров для всех расценок из таблицы """
    cursor = db.go_execute(sql_queries["get_options_table_id"], (table_id,))
    result = cursor.fetchall() if cursor else None
    return tuple([row['option'] for row in result]) if result else None


def get_values_options_for_table(db: dbTolls, options_name: str, table_id: int) -> tuple[str, ...] | None:
    """ Получить все значения (от, до, шаг, тип) параметра для всех расценок в таблице """
    cursor = db.go_execute(sql_queries["get_values_options_name_table_id"], (options_name, table_id))
    result = cursor.fetchall() if cursor else None
    return tuple([tuple(row) for row in result]) if result else None

















