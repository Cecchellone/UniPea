import os
import datetime
import sqlite3

database = sqlite3.connect("UniPea.db")

path = os.path.dirname(os.path.realpath(__file__))

def get_query(sql_file_name, **kwargs):
    var_identifier = "#"
    query = ""
    with open(os.path.join(os.getcwd(), sql_file_name), 'r') as sql_file:
        query = sql_file.read()
        for key, val in kwargs.items():
            query = query.replace(var_identifier + key, str(val))
    return query

def TimeTable(name, weekday):
    query = get_query(os.path.join(path, "GetOrari.sql"), name=name, weekday=weekday)
    row = database.execute(query).fetchone()[1:]
    #return row
    table = [datetime.timedelta(minutes=x) for x in row if x is not None]
    if len(table) == 2:
        return tuple(table), None
    elif len(table) == 4:
        return tuple(table[2:]), tuple(table[:2])
    else:
        return None

def EndDay(name):
    query = get_query(os.path.join(path, "end_day.sql"), name=name)
    result = database.execute(query).fetchone()
    if result is None:
        return None, None, None
    else:
        return result[0], result[1], (result[2] is not None and result[2]>=1)

'''
pranzo, cena = TimeTable("centrale", 5)
print(pranzo[0], pranzo[1])
if cena is not None:
    print(cena[0], cena[1])
'''