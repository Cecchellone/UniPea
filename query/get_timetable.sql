select distinct ID, LunchStart, LunchEnd, DinnerStart, DinnerEnd
from Keys
	natural join Synonyms
	natural join Timetable
Where Name = "#name"
	and (WeekDay isnull or WeekDay like "%#weekday%")
	--#kind and Kind = "#kind"