
from openpyxl.worksheet import worksheet
from openpyxl.utils.cell import column_index_from_string
from openpyxl.styles import DEFAULT_FONT
import openpyxl

from db.get_data_db import get_data_db
from files_tolls import output_message_exit, file_unused



def _basic_header_output(sheet: worksheet):
    sheet.append(["."])
    header = ["Шифр ПСМ", "Наименование ПСМ", "Номер позиции в ПСМ", "Наименование ресурса", "Измеритель", "файл"]
    sheet.append(header)
    for col in ['A', 'B', 'C', 'D', 'E', 'F']:
        sheet.column_dimensions[col].width = 25


def _data_line_output(sheet: worksheet, src_data: tuple, start_row: int) -> int:
    sheet.cell(row=start_row, column=column_index_from_string('A')).value = src_data[0]
    sheet.cell(row=start_row, column=column_index_from_string('B')).value = src_data[1]
    sheet.cell(row=start_row, column=column_index_from_string('C')).value = src_data[2]
    sheet.cell(row=start_row, column=column_index_from_string('D')).value = src_data[3]
    sheet.cell(row=start_row, column=column_index_from_string('E')).value = src_data[4]
    sheet.cell(row=start_row, column=column_index_from_string('F')).value = src_data[5]
    return 1


def write_excel_file(excel_file_name: str, path_db: str):
    if file_unused(excel_file_name):
        book, sheet = None, None
        try:
            book = openpyxl.Workbook()
            DEFAULT_FONT.font = "Calibri"
            DEFAULT_FONT.sz = 8
            sheet = book.active # получить ссылку на активную книгу
            sheet.title = "data"
        except IOError as err:
            output_message_exit(f"Ошибка при создании excel файла: {excel_file_name!r}", f"{err}")
        # получить данные из БД
        data_set = get_data_db(path_db)
        if data_set:
            # вывод шапки таблицы
            _basic_header_output(sheet)
            x = 4
            for row in data_set:
                x += _data_line_output(sheet, row[1:], x)

        if book:
            book.save(excel_file_name)
            book.close()
    else:
        output_message_exit(f"Файл занят другим приложением: ", f"{excel_file_name!r}")






if __name__ == "__main__":
    db_path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\PSM_Parsing\output\PSM.sqlite3"
    write_excel_file("test.xlsx", db_path)