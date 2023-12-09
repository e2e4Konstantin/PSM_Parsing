
sql_queries = {
    "get_table_id": """
        SELECT c.ID_tblCatalog
        FROM tblCatalogs c
        WHERE
            c.FK_tblCatalogs_tblDirectoryItems = (
                SELECT di.ID_tblDirectoryItem FROM tblDirectoryItems di WHERE di.name = 'Таблица'
                )
                AND c.code REGEXP ?; --'^4\.8-\d+-\d+-0-288'
        """,

    "count_number_table_quotes_by_id": """
        SELECT COUNT(*) AS number FROM tblQuotes q WHERE  q.FK_tblQuotes_tblCatalogs = ?;
        """,



    "get_attributes_table_id": """
        SELECT DISTINCT a.name AS attribute
        FROM tblAttributes a
        WHERE a.FK_tblAttributes_tblQuotes IN (
            SELECT q.ID_tblQuote FROM tblQuotes q WHERE q.FK_tblQuotes_tblCatalogs = ?
        );
        """,

    "get_attributes_table_code": """
        SELECT
          DISTINCT a.name AS attribute
        FROM
          tblAttributes a 
        WHERE
          a.FK_tblAttributes_tblQuotes IN (
              SELECT
                q.ID_tblQuote
              FROM
                tblQuotes q 
              WHERE
                q.FK_tblQuotes_tblCatalogs = (
                    SELECT
                      c.ID_tblCatalog
                    FROM
                      tblCatalogs c 
                    WHERE
                      c.FK_tblCatalogs_tblDirectoryItems = (
                          SELECT
                            di.ID_tblDirectoryItem
                          FROM
                            tblDirectoryItems di 
                          WHERE
                            di.name = 'Таблица'
                        )
                      AND c.code REGEXP ?
                  )
            );    
    """,

    "get_value_attribute_count_name_table_id": """
        SELECT
          COUNT(DISTINCT a.value)
        FROM
          tblAttributes a
        WHERE
          a.name = ?
          AND a.FK_tblAttributes_tblQuotes IN (
              SELECT
                q.ID_tblQuote
              FROM
                tblQuotes q
              WHERE
                q.FK_tblQuotes_tblCatalogs = ?
            );    
    """,

    "get_values_attribute_name_table_id": """
        SELECT a.value AS value
        FROM tblAttributes a
        WHERE
          a.name = ?
          AND a.FK_tblAttributes_tblQuotes IN (
              SELECT q.ID_tblQuote
              FROM tblQuotes q
              WHERE q.FK_tblQuotes_tblCatalogs = ?
            );    
    """,
    # --- > Options ---------------------------------------------------------------------

    "get_options_table_id": """
        SELECT DISTINCT o.name AS option 
        FROM tblOptions o
        WHERE o.FK_tblOptions_tblQuotes IN (
            SELECT q.ID_tblQuote FROM tblQuotes q WHERE q.FK_tblQuotes_tblCatalogs = ?  
        );
        """,

    "get_values_options_name_table_id": """
        SELECT o.left_border, o.right_border, o.measurer, o.step --o.name,  
        FROM tblOptions o
        WHERE
          o.name = ?
          AND o.FK_tblOptions_tblQuotes IN (
              SELECT q.ID_tblQuote
              FROM tblQuotes q
              WHERE q.FK_tblQuotes_tblCatalogs = ?
            );
        """,


}
