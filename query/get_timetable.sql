select distinct LunchStart, LunchEnd, DinnerStart, DinnerEnd
from Timetable
Where Name = "#name"
	and (WeekDay isnull or WeekDay like "%#weekday%")
	--#kind and Kind = "#kind"