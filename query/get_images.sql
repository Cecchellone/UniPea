SELECT Image, Meal --PDF
FROM Images
WHERE ID = "#name" AND
	Expire > #expire
	--#meal AND Meal = "#meal"
GROUP BY ID
HAVING MAX(Expire)
ORDER BY Page