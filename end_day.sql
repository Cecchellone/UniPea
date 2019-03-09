SELECT DISTINCT ID, EndDay, Splitted
FROM Keys NATURAL JOIN Synonyms
WHERE Names = "#name"