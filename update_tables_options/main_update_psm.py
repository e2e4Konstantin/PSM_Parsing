from icecream import ic
import os

from update_tables_options.build_files_list import build_files_list_by_mask
from update_tables_options.psm_file_tools import psm_restore


def update_psm_tables(psm_files_path: str, db_file_name: str):
    psm_file_name_mask = r"[^~].*[\d+]((\d+-){4}).*\.xlsx"
    psm_roll = build_files_list_by_mask(psm_files_path, psm_file_name_mask)
    # ic(psm_roll)
    for psm_file in psm_roll:
        psm_restore(psm_file, db_file_name)


if __name__ == "__main__":
    db_path = r"F:\Kazak\GoogleDrive\Python_projects\DB"
    db_name = os.path.join(db_path, "quotes_test.sqlite3")
    ic(db_name)
    psm_files_location = r"F:\Kazak\GoogleDrive\NIAC\Велесь_Игорь\ПСМ"
    ic(psm_files_location)
    update_psm_tables(psm_files_location, db_name)
