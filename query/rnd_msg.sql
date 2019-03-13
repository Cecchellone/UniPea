select Text
from Msgs
where Name ISNULL OR Name = "#name"
order by random()
limit 1