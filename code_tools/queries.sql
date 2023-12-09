SELECT
  DISTINCT a.name
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
    )
;
SELECT
  COUNT(DISTINCT a.value)
FROM
  tblAttributes a
WHERE
  a.name = 'Способ'
  AND a.FK_tblAttributes_tblQuotes IN (
      SELECT
        q.ID_tblQuote
      FROM
        tblQuotes q
      WHERE
        q.FK_tblQuotes_tblCatalogs = 4892
    )
;

SELECT COUNT(*) FROM tblQuotes q WHERE  q.FK_tblQuotes_tblCatalogs = 5048
