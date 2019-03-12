import os
import datetime
import sqlite3

database = sqlite3.connect("UniPea.db")
database.row_factory = sqlite3.Row

working_path   = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(working_path, "query")

def time_to_minutes(var):
    if isinstance(var, datetime.datetime):
        return (var.minute + var.hour*60)
    elif type(var) == int:
        return datetime.timedelta(minutes=var)

def get_query(sql_file_name, **kwargs):
    rem_identifier = "--#"
    var_identifier = "#"
    query = ""
    with open(os.path.join(os.getcwd(), sql_file_name), 'r') as sql_file:
        query = sql_file.read()
        for key, val in kwargs.items():
            query = query.replace(rem_identifier + key, "")
            query = query.replace(var_identifier + key, str(val))
    return query

def TimeTable(name, weekday, **kwargs):
    '''kind -> "PV" prendi e vai'''
    query = get_query(os.path.join(path, "get_timetable.sql"), name=name, weekday=weekday, **kwargs)
    row = database.execute(query).fetchone()
    if row is None:
        return None
    #return row
    times = ["LunchStart", "LunchEnd", "DinnerStart", "DinnerEnd"]
    table = [datetime.timedelta(minutes=row[x]) for x in times if row[x] is not None]
    if len(table) == 2:
        return tuple(table), None
    elif len(table) == 4:
        return tuple(table[2:]), tuple(table[:2])
    else:
        return None, None

def EndDay(name):
    query = get_query(os.path.join(path, "end_day.sql"), name=name)
    result = database.execute(query).fetchone()
    if result is None:
        return None, None, None
    else:
        return result["ID"], result["EndDay"], (result["Splitted"] is not None and result["Splitted"]>=1)

def NowOpen(date, **kwargs):
    query = get_query(os.path.join(path, "now_open.sql"), weekday=date.weekday(), minutes=time_to_minutes(date), **kwargs)
    #return [tuple([x["ID"], x["kind"]]) for x in database.execute(query).fetchall()]
    result = []
    for name, kind in database.execute(query).fetchall():
        if kind is None:
            kind = 'M'
        if len(result) > 0 and name == result[-1][0]:
            result[-1][1].append(kind)
        else:
            result.append((name, [kind]))
    return result

'''
for x in NowOpen(datetime.datetime.now() - datetime.timedelta(minutes=30), ):
    print(*x, sep='\t')

print(TimeTable("martiri", 4, kind="PV"))

pranzo, cena = TimeTable("centrale", 5)
print(pranzo[0], pranzo[1])
if cena is not None:
    print(cena[0], cena[1])
'''