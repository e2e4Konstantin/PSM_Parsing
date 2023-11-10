
# design budget module
create_table = {
    "create_moduls": """
        CREATE TABLE IF NOT EXISTS tblModuls ( 
            ID_tblModul   INTEGER PRIMARY KEY NOT NULL,
            code          TEXT    NOT NULL,
            description   TEXT    NOT NULL,
            measure       TEXT    NOT NULL,
            UNIQUE (code)
        );""",

    "create_modul_items": """
        CREATE TABLE IF NOT EXISTS tblModulItems ( 
            ID_tblModulItem   INTEGER PRIMARY KEY NOT NULL,
            code           TEXT    NOT NULL,
            description    TEXT    NOT NULL,
            measure        TEXT    NOT NULL,
            matching       TEXT    NOT NULL,
            volume_factor  TEXT    NOT NULL,
            criteria       TEXT    NOT NULL,
            pilot          TEXT    NOT NULL,
            FK_tblModulItems_tblModuls    INTEGER NOT NULL,
            FOREIGN KEY (FK_tblModulItems_tblModuls) REFERENCES tblModulItems (ID_tblModul),
            UNIQUE (code)
        );""",

    # "Шифр ПСМ", "Наименование ПСМ", "Номер позиции в ПСМ", "Наименование ресурса", "Измеритель"
    "create_raw_parse": """
        CREATE TABLE IF NOT EXISTS tblRawParsers ( 
            ID_tblRawParser      INTEGER PRIMARY KEY NOT NULL,
            psm_code             TEXT    NOT NULL,
            psm_description      TEXT    NOT NULL,
            position_number      TEXT    NOT NULL,  
            resource_description TEXT    NOT NULL,
            measure              TEXT,
            file_name            TEXT    NOT NULL
        );""",

}

insert_query = {
    "insert_raw_parsers": """
        INSERT INTO tblRawParsers (psm_code, psm_description, position_number, resource_description, measure, file_name)
        VALUES (?, ?, ?, ?, ?, ?);
    """,
}

select_query = {
    "select_all_raw_parsers": """SELECT * FROM tblRawParsers;""",
}

