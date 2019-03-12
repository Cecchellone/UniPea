select ID, Kind
from Timetable
	--#name natural join Synonims
where (WeekDay ISNULL OR WeekDay like ('%#weekday%')) AND 
	((
		LunchStart <= #minutes AND LunchEnd > #minutes
	) OR (
		DinnerStart NOTNULL AND DinnerEnd NOTNULL AND
		DinnerStart <= #minutes AND DinnerEnd > #minutes
	))
	--#name AND Names = #name
order by ID;