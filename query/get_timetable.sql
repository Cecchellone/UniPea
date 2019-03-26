select WeekDay, Kind, LunchStart, LunchEnd, DinnerStart, DinnerEnd
from Timetable
Where Name = "#name"
	--#weekday and (WeekDay isnull or WeekDay like "%#weekday%")
	--#kind and Kind = "#kind"