SELECT *
FROM Files
    natural join Structures
WHERE ID= "#id"
    AND Expire = "#expire";