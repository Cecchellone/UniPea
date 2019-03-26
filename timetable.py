import locale
import calendar
import datetime
import db_reader as dbr
from string import Template

class DeltaTemplate(Template):
    delimiter = "%"

locale.setlocale(locale.LC_ALL, "it_IT")

def time_to_minutes(var):
    if isinstance(var, datetime.datetime):
        return (var.minute + var.hour*60)
    elif type(var) == int:
        return datetime.timedelta(minutes=var)

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)

def weekstring(code):
    days = code
    if type(code) == str:
        days = [str(num) in code for num in range(7)]
    elif type(code) != list:
        return
    qta = sum(days)

    if qta<=0:      #NESSUNO
        return
    #if qta==7:      #TUTTI
    #    return "tutta la settimana"
    elif qta==1:    #SINGOLO
        return calendar.day_name[days.index(True)]
    elif qta==2:    #DOPPIO
        index = days.index(True)
        days[index] = False
        return calendar.day_name[index] + ", " + weekstring(days)
    else:           #MULTIPLI (non per forza adiacenti)
        start = days.index(True)
        text = ""
        if start+2 <7 and all(days[start:start+2]): #SEQUENZA INDIVIDUATA (minimo: 3) 
            i = start
            while i < 7 and days[i]==True:
                days[i] = False
                i += 1
            text = calendar.day_name[start] + " - " + calendar.day_name[i-1]
        else:   #SEQUENZA NON INDIVIDUATA (ripeto la funzione su un unsieme più piccolo: 2)
            internal = [False]*7

            for i in [start, start+1]:
                internal[i] = days[i]
                days[i] = False
            text = weekstring(internal)

        if any(days):   #Controllo di aver controllato tutti i valori
           text += ", " + weekstring(days)
        return text

def writemeal(Minutes, **kwargs):
    form = "%k:%M"
    #if "fixed" in kwargs and kwargs.get("fixed"):
    #    form = "%H:%M"
    text = (datetime.datetime.fromtimestamp(0) + time_to_minutes(Minutes)).strftime(form)
    #if text.startswith("0"):
    #    text = " " + text[1:]
    return text

def makeperiod(WD, LS, LE, DS, DE):
    text = weekstring(WD) + "\n"
    if LS is not None and LE is not None:
        text += "Pranzo:"
        text += "\t" + writemeal(LS) + " -> " + writemeal(LE) + "\n"
    if DS is not None and DE is not None:
        text += "Cena:"
        text += "\t" + writemeal(DS) + " -> " + writemeal(DE) + "\n"
    return text
    
'''
A = ("01234", 705, 870, 1140, 1275)
B = ("5", 720, 870, None, None)
C = ("6", 720, 870, 1140, 1275)

print(makeperiod(*A))
print(makeperiod(*B))
print(makeperiod(*C))
'''