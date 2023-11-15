
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

    "create_raw_parse": """
        CREATE TABLE IF NOT EXISTS tblRawParsers ( 
            ID_tblRawParser         INTEGER PRIMARY KEY NOT NULL,
            psm_code                TEXT NOT NULL,  -- псм шифр
            psm_description         TEXT NOT NULL,  -- псм наименование
            psm_measure             TEXT,           -- псм измеритель
            item_number             TEXT,           -- номер позиции
            item_code               TEXT,           -- шифр позиции
            item_description        TEXT,           -- наименование
            item_measure            TEXT,           -- измеритель
            comparison              TEXT,           -- сопоставление параметров и атрибутов
            volume_formula          TEXT,           -- формула объема
            notes                   TEXT,           -- пояснения/шифр расценки
            criteria                TEXT,           -- критерии/сценарии
            inspection              TEXT,           -- проверка на пилоте
            file_name               TEXT NOT NULL, 
            row_number              INTEGER NOT NULL
        );""",

    # Note that if you need strict typing, you can always add a constraint like CHECK(typeof(mycol) = 'integer').
    # для хранения информации о файле
    "create_files_info": """
        CREATE TABLE IF NOT EXISTS tblFilesInfo (
	        ID_tblFilesInfo INTEGER PRIMARY KEY NOT NULL, 
	        file_name       TEXT NOT NULL, 
	        row_numbers     TEXT, 
	        target_quantity INTEGER DEFAULT 0, 
	        CHECK(TYPEOF(target_quantity) == 'INTEGER'), 
	        UNIQUE (file_name)
	    );""",

}


insert_query = {
    "insert_raw_parsers": """
        INSERT INTO tblRawParsers (
            psm_code, 
            psm_description, 
            psm_measure, 
            item_number, 
            item_code, 
            item_description, 
            item_measure, 
            comparison, 
            volume_formula, 
            notes, 
            criteria, 
            inspection, 
            file_name, 
            row_number
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """,
}

select_query = {
    "select_all_raw_parsers": """SELECT * FROM tblRawParsers;""",
    "select_P6_raw_parsers": """SELECT * FROM tblRawParsers WHERE criteria is 'Р6';""",
    "select_count_P_raw_parsers": """
        SELECT file_name, 
            count(distinct ID_tblRawParser) AS 'всего',
            sum(case when criteria = 'Р1' then 1 else 0 end) AS P1,
            sum(case when criteria = 'Р2' then 1 else 0 end) AS P2,
            sum(case when criteria = 'Р3' then 1 else 0 end) AS P3,
            sum(case when criteria = 'Р4' then 1 else 0 end) AS P4,
            sum(case when criteria = 'Р5' then 1 else 0 end) AS P5,
            sum(case when criteria = 'Р6' then 1 else 0 end) AS P6
        FROM tblRawParsers
        GROUP BY file_name;    
    """,

    "select_unic_criteria": """
        SELECT DISTINCT criteria 
        FROM tblRawParsers
        WHERE criteria LIKE 'С%' OR criteria LIKE 'Р%';
        --ORDER BY criteria;
    """,
}

# -- SELECT file_name, count(file_name) AS 'счетчик Р6' FROM tblRawParsers WHERE criteria is 'Р6' GROUP BY file_name;
#
# -- SELECT file_name, count(distinct ID_tblRawParser) AS 'счетчик Р6' FROM tblRawParsers WHERE criteria is 'Р6' GROUP BY file_name;

# SELECT m.file_name,
# 	   (SELECT count(*) FROM tblRawParsers WHERE file_name=m.file_name) AS 'всего',
# 	   (SELECT count(*) FROM tblRawParsers WHERE file_name=m.file_name AND criteria = 'Р1') AS 'P1',
# 	   (SELECT count(*) FROM tblRawParsers WHERE file_name=m.file_name AND criteria = 'Р2') AS 'P2',
# 	   (SELECT count(*) FROM tblRawParsers WHERE file_name=m.file_name AND criteria = 'Р3') AS 'P3',
# 	   (SELECT count(*) FROM tblRawParsers WHERE file_name=m.file_name AND criteria = 'Р4') AS 'P4',
# 	   (SELECT count(*) FROM tblRawParsers WHERE file_name=m.file_name AND criteria = 'Р5') AS 'P5',
# 	   (SELECT count(*) FROM tblRawParsers WHERE file_name=m.file_name AND criteria = 'Р6') AS 'P6'
# FROM (SELECT DISTINCT file_name FROM tblRawParsers) as m
