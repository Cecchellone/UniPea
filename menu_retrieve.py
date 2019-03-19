import os
import asyncio
import time
import datetime
import urllib.request
import io
from pdf2image import convert_from_path as cfp
from PIL import Image
import db_reader as dbr

working_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(working_path, "images")
if not os.path.isdir(path):
    os.mkdir(path)

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

async def save_png(images, name):
    dbr.add_image(images, name, None, datetime.datetime.now())
    return len(images)

async def makeimg(mensa_name):
    mensa_name = mensa_name.lower()
    #path = os.path.dirname(os.path.realpath(__file__))
    url = geturl(datetime.datetime.now(), mensa_name)
    print("Url:", url)

    pdf_name = await retrieve_file(url, 24, 3600)

    if pdf_name != "":
        print("Converting pages")
        pages = cfp(pdf_name, 500)
        await save_png(pages, mensa_name + ".png")
        print("Menù exported")
        os.remove(pdf_name)
        print("Cleared temporary files")
        return os.path.join(path, mensa_name + ".png")
    else:
        print("Unable to find the menù")
        return

files = ["images\\cammeo.png"]
pages = [Image.open(os.path.join(working_path, x)) for x in files]
asyncio.run(save_png(pages, "cammeo"))
'''
#asyncio.run(makeimg(input("Type mensa name: ")))
'''