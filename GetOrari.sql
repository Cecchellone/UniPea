select distinct ID, LunchStart, LunchEnd, DinnerStart, DinnerEnd
from Keys
	natural join Synonyms
	natural join Timetable
Where Names = "#name"
	and (WeekDay isnull or WeekDay like "%#weekday%")
	--#kind and Kind = "#kind"