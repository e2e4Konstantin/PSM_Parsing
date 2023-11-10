import os
from icecream import ic
from db import read_data
from excel_tools import write_excel_file


def get_place_point() -> tuple[str, str, str]:
    data_files_location = r"F:\Kazak\GoogleDrive\NIAC\PSM"
    db_name = "PSM.sqlite3"
    output_name = "psm_parsing.xlsx"
    db_path = os.path.join(os.path.dirname(__file__), "output", db_name)
    output_excel_file_name = os.path.join(data_files_location, output_name)
    return data_files_location, db_path, output_excel_file_name


if __name__ == "__main__":
    src_data_path, db_file_name, excel_file_name = get_place_point()
    ic(src_data_path, db_file_name)
    read_data(src_data_path, db_file_name)
    write_excel_file(excel_file_name, db_file_name)
