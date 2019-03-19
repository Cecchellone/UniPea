SELECT DISTINCT ID, EndDay, Splitted
FROM Menus NATURAL JOIN Structures
WHERE Name = "#name"