import re
from fastnumbers import isfloat, isint

_re_compiled_patterns = {
    'subsection_groups': re.compile(r"(^\d+\.\d+-\d+-)(\d+)\s*"),
    'wildcard': re.compile(r"[\t\n\r\f\v\s+]+"),
    'code_valid_chars': re.compile(r"[^\d+.-]+"),
    'digits': re.compile(r"[^\d+]+"),
    'digits_dots': re.compile(r"[^\d+.]+"),
}


def remove_wildcard(source: str = None) -> str | None:
    """ Удаляет из строки переносы строк и табуляции, одиночные пробелы оставляет """
    return re.sub(_re_compiled_patterns['wildcard'], r" ", source.strip()) if source else None


def clear_code(source: str = None) -> str | None:
    """ Удаляет из строки все символы кроме (чисел, '.', '-') """
    return re.sub(_re_compiled_patterns['code_valid_chars'], r"", source)


def keep_just_numbers(source: str = None) -> str | None:
    """ Удаляет из строки все символы кроме чисел """
    if source:
        return re.sub(_re_compiled_patterns['digits'], r"", source)
    return ""


def keep_just_numbers_dots(source: str = None) -> str | None:
    """ Удаляет из строки все символы кроме чисел и точек"""
    if source:
        return re.sub(_re_compiled_patterns['digits_dots'], r"", source)
    return ""


def text_cleaning(text: str) -> str | None:
    """ Удаляет из заголовка служебные символы и лишние пробелы. """
    text = remove_wildcard(text)
    if text:
        return " ".join(text.split())
    return None


def split_code(src_code: str) -> tuple:
    """ Разбивает шифр на части. '4.1-2-10' -> ('4', '1', '2', '10')"""
    if src_code:
        return tuple([x for x in re.split('[.-]', src_code) if x])
    return tuple()

def split_code_int(src_code: str):
    """ Разбивает шифр на части из чисел. '4.1-2-10' -> (4, 1, 2, 10)"""
    return tuple(map(int, re.split('[.-]', src_code))) if src_code else tuple()


def identify_item(src_code: str) -> tuple:
    """ Определяет по шифру категорию записи. """
    # ['5',       '5.1',          '5.1-1',    '5.1-1-1',      '5.1-1-1-0-1',  '5.1-1-1']
    # ['chapter', 'collection',   'section',  'subsection',   'table',        'quote']
    code = remove_wildcard(src_code)
    if code:
        length = len(split_code(code))
        match length:
            case 6:  # таблица
                extract = ('table',)
            case 4:  # раздел, расценка
                extract = ('subsection', 'quote')
            case 3:  # отдел
                extract = ('section',)
            case 2:  # сборник
                extract = ('collection',)
            case 1:  # глава
                extract = ('chapter',)
            case _:  # непонятно
                extract = tuple()
        return extract
    return tuple()


def check_code_item(src_code: str, item_name) -> bool:
    """ Проверяет, соответствует ли код указанному типу"""
    check_types = identify_item(src_code)
    if len(check_types) > 0 and check_types[0] == item_name:
        return True
    return False


def get_float_value(value: str) -> float:
    """ Конвертирует строку в число с плавающей точкой. """
    if value:
        value = value.replace(',', '.', 1)
        return float(value) if isfloat(value) else 0.0
    return 0.0


def get_integer_value(value: str) -> int:
    """ Конвертирует строку в целое число. """
    return int(value) if isint(value) else 0


if __name__ == "__main__":
    from icecream import ic

    c = '5.1-2-8'
    s = '5  . 1-1 .**-1-0-   1   '
    ic(keep_just_numbers(s))
    ic(keep_just_numbers_dots(s))

    ic(remove_wildcard(s))

    ic(split_code(c))

    ic(clear_code(s))
    ic(clear_code(""))

    # print(items_data.keys())
    # print([x for x in items_data.keys()])
    # print(items_data['table'].prefix)
    # test = ['5', '5.1', '5.1-1', '5.1-1-1', '5.1-1-1-0-1', '5.1-1-1']
    # for x in test:
    #     print(identify_item(x))
