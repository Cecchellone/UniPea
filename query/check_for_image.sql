SELECT *
FROM Files
    natural join Structures
WHERE Expire = #expire
    --#id AND ID= "#id"
    --#name AND Name= "#name"