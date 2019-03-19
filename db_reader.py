import os
import io
import datetime
import sqlite3
from PIL import Image

working_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(working_path, "query")

database = sqlite3.connect("UniPea.db")
database.row_factory = sqlite3.Row

build_users = not os.path.isfile(os.path.join(working_path, "Users.db"))
user_db = sqlite3.connect("Users.db")
user_db.row_factory = sqlite3.Row
if build_users:
    with open(os.path.join(path, "Users.db.sql"), 'r') as sql_file:
        user_db.executescript(sql_file.read())

def clean(text):
    return str(text).strip().lower()

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

def exist_image(expire, **kwargs):
    query = get_query(os.path.join(path, "check_for_image.sql"), expire=expire, **kwargs)
    print(query)
    if database.execute(query) is not None:
        return False
    else:
        return True

def add_user(info):
    timestamp = int(datetime.datetime.now().timestamp())

    q_find = "SELECT COUNT(*) FROM Users WHERE UID = ? ;"
    if user_db.execute(q_find, (info['id'],)).fetchone()[0] <= 0:
        query = "INSERT OR REPLACE INTO Users(UID, Name, Subscription, LastAccess) VALUES(?, ?, ?, ?);"
        name = info['first_name']
        if 'username' in info.keys():
            name = info['username']
        elif 'last_name' in info.keys():
            name = name + " " + info['last_name']
            
        user_db.execute(query, (info['id'], name, timestamp, timestamp))
        #print("added", username)
    else:
        query = "UPDATE Users SET LastAccess = ? WHERE UID = ?;"
        user_db.execute(query, (timestamp, info['id']))
    user_db.commit()

def add_image(images, MID, meal, expire):
    end_date = int((expire.replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)).timestamp())
    #ID, Meal, Page, Expire, Image

    #if exist_image(end_date, name=MID):
    #    print("image already on DB")
    #    return
    #search_query = get_query(os.path.join(path, "check_for_image.sql"), name=MID, expire=expire)
    #if database.execute(search_query) is not None:
    #    return

    query = "INSERT OR REPLACE INTO Files VALUES(?, ?, ?, ?, ?, ?);"
    for index, image in enumerate(images):
        stream = io.BytesIO()
        image.save(stream, "PNG")
        stream.seek(0)
        database.execute(query, (get_id(MID), meal, index, end_date, sqlite3.Binary(stream.getvalue()), None))
    database.commit()
    #file = cursor.execute('select bin from File where id=?', (id,)).fetchone()

def get_image(name, **kwargs):
    timestamp = datetime.datetime.now().timestamp()
    MID= get_id(name)
    query = get_query(os.path.join(path, "get_images.sql"), id=MID, expire=int(timestamp), **kwargs)
    cursor = database.execute(query)
    images = []
    for row in cursor:
        img_stream = io.BytesIO()
        #pdf_stream = io.BytesIO()
        img_stream.write(row['Image'])
        #pdf_stream.write(row['pdf'])
        images.append(Image.open(img_stream))
    return images

def get_id(name):
    output = database.execute("select ID from Structures where Name = '" + clean(name) + "'").fetchone()
    if output is None:
        return None
    else:
        return str(output[0])

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

def RndMsg(name):
    query = get_query(os.path.join(path, "rnd_msg.sql"), name=name.lower())
    result = database.execute(query).fetchone()
    if result is None:
        return None
    else:
        return str(result["Text"])
'''
Image._show(get_image("cammeo")[0])

with open(os.path.join(working_path, "images\\cammeo.png"), 'rb') as imgfile:
    add_image([imgfile.read()], "cammeo", None, datetime.datetime.now())        

while True:
    print(RndMsg(input("nome mensa: ")))

for x in NowOpen(datetime.datetime.now() - datetime.timedelta(minutes=30), ):
    print(*x, sep='\t')

print(TimeTable("martiri", 4, kind="PV"))

pranzo, cena = TimeTable("centrale", 5)
print(pranzo[0], pranzo[1])
if cena is not None:
    print(cena[0], cena[1])
'''