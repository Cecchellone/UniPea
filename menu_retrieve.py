import os
import asyncio
import time
import datetime
import urllib.request
from pdf2image import convert_from_path as cfp
import db_reader as dbr
   
def getperiod(end_day):
    Today = datetime.datetime.now()

    if end_day is not None:
        Lastmon = Today   - datetime.timedelta(days=Today.weekday())
        EndDay  = Lastmon + datetime.timedelta(days=end_day)
        return Lastmon, EndDay
    return ValueError

def geturl(date, name):
    base_url = "http://www.dsu.toscana.it/it/Men%C3%B9"
    ID, end_day, splitted = dbr.EndDay(name)
    begin, end = getperiod(end_day)
    #if not splitted:
    return base_url + "-dal-" + begin.strftime("%d.%m.%y") + "-al-" + end.strftime("%d.%m.%y") + "-" + ID + ".pdf"

async def retrieve_file(url, retry_attempts, retry_interval):
    for i in range(retry_attempts):
        print("attempt", i+1, "of", retry_attempts)
        try:
            file_name, headers = urllib.request.urlretrieve(url)
            print("Menù retrieved")
            return file_name
        except:
            print("Menù not found, retrying in", retry_interval, "seconds")
            await asyncio.sleep(retry_interval)
    else:
        print("Unable to locate the file")
        return ""

async def save_png(pages, path, name):
    page_num = len(pages)

    for i, page in enumerate(pages):
        print("Exporting page", i+1, "of", page_num)
        file_name = name
        if page_num >1:
            file_name = "{0}_{2}.{1}".format(*os.path.splitext(name) + [i])
        page.save(os.path.join(path, file_name), "PNG")
    return page_num

async def makeimg(mensa_name):
    mensa_name = mensa_name.lower()
    path = os.path.dirname(os.path.realpath(__file__))
    url = geturl(datetime.datetime.now(), mensa_name)
    print("Url:", url)

    pdf_name = await retrieve_file(url, 24, 3600)

    if pdf_name != "":
        print("Converting pages")
        pages = cfp(pdf_name, 500)
        await save_png(pages, path, mensa_name + ".png")
        print("Menù exported")
        os.remove(pdf_name)
        print("Cleared temporary files")
        return os.path.join(path, mensa_name + ".png")
    else:
        print("Unable to find the menù")
        return

#asyncio.run(makeimg(input("Type mensa name: ")))