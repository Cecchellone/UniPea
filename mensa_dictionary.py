import datetime
import db_reader as dbr

def week_mode(name, end_day):
    base_url = "http://www.dsu.toscana.it/it/Men%C3%B9"
    Today = datetime.datetime.now()
    Lastmon = Today - datetime.timedelta(days=Today.weekday())
    Nextsun = Lastmon + datetime.timedelta(days=end_day)
    return base_url + "-dal-" + Lastmon.strftime("%d.%m.%y") + "-al-" + Nextsun.strftime("%d.%m.%y") + "-" + name + ".pdf"

def translator(mensa_name):
    #Weekly
    name, end_day, splitted = dbr.EndDay(mensa_name)
    
    if name is None:
        return "Not found"
    elif end_day is not None:
        if splitted:
            return [week_mode("pranzo-"+ name, end_day), week_mode("cena-"+ name, end_day)]
        else:
            return week_mode(name, end_day)

    #prato
    #praticelli
    #carrara
    #lucca  
    
print(translator("cammeo"))