import os
import re

from icecream import ic
from openpyxl.worksheet import worksheet
from openpyxl import load_workbook
from openpyxl.utils.cell import column_index_from_string
from files_tolls import output_message_exit, output_message


def _get_data_line(work_sheet: worksheet, target_row: int) -> tuple:
    psm_code = work_sheet['D2'].value
    psm_title = work_sheet['D3'].value
    number = work_sheet.cell(row=target_row, column=column_index_from_string('A')).value
    title = work_sheet.cell(row=target_row, column=column_index_from_string('C')).value
    measure = work_sheet.cell(row=target_row, column=column_index_from_string('D')).value
    return psm_code, psm_title, number, title, measure


def get_data_from_excel(file_name: str) -> list[tuple]:
    book, sheet = None, None
    sheet_name = "ОГ"
    mask_name = re.compile(r"^\s*(ОГ)|(OГ)\s*")
    marker = "Р6"
    result = []
    try:
        book = load_workbook(filename=file_name, data_only=True)
        sheets = book.sheetnames
        ts = [x for x in sheets if mask_name.match(x)]
        if len(ts) > 0:
            book[ts[0]].title = sheet_name
            sheet = book[sheet_name]
            # ic(sheet.title)
            # ic(sheet.max_row, sheet.max_column)
            column_m = column_index_from_string('M')
            target_rows = [row
                           for row in range(1, sheet.max_row + 1)
                           if sheet.cell(row=row, column=column_m).value == marker
                           ]
            base_file_name = os.path.basename(file_name)
            ic(base_file_name, target_rows)
            for row in target_rows:
                result.append(_get_data_line(sheet, row)+(base_file_name, ))
            # ic(result)
        else:
            output_message(f"В excel файле: {file_name!r}", f"нет страницы: {sheet_name!r}")
        book.close()
        return result
    except IOError as err:
        output_message_exit(f"Ошибка при открытии excel файла: {file_name!r}", f"{err}")
    return []












