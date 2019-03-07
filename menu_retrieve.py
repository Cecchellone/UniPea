import os
import asyncio
import time
import datetime
import urllib.request
from pdf2image import convert_from_path as cfp
   
def geturl(date, name):
    base_url = "http://www.dsu.toscana.it/it/Men%C3%B9"
    
    Today = datetime.datetime.now()
    Lastmon = Today - datetime.timedelta(days=Today.weekday())
    Nextsun = Lastmon + datetime.timedelta(days=6)
    
    PM = Lastmon.strftime("%d.%m.%y")
    PS = Nextsun.strftime("%d.%m.%y")
    return base_url + "-dal-" + PM + "-al-" + PS + "-" + name + ".pdf"

async def retrieve_file(url, retry_attempts, retry_interval):
    for i in range(retry_attempts):
        print("attempt:", i+1, "of", retry_attempts)
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

async def makeimg(mensa_name):
    path = os.path.dirname(os.path.realpath(__file__))
    url = geturl(datetime.datetime.now(), mensa_name)
    print("Url:", url)

    pdf_name = await retrieve_file(url, 24, 3600)

    if pdf_name != "":
        pages = cfp(pdf_name, 500)
        pages[0].save(path + "/" + mensa_name + ".jpg", "JPEG")
        print("Menù exported")
        os.remove(pdf_name)
        print("Cleared temporary files")
    else:
        print("Unable to find the menù")

asyncio.run(makeimg("martiri"))