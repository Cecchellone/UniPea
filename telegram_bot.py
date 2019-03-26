import asyncio
import os
import io
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
import menu_retrieve as getmen
import db_reader as dbr
import timetable as ttb

class Answerer(telepot.aio.helper.ChatHandler):
    Flow = {}
    
    def __init__(self, *args, **kwargs):
        super(Answerer, self).__init__(*args, **kwargs)

    async def on_chat_message(self, msg):
        chat_id = msg['chat']['id']
        #user_name = msg['chat']['username']
        #real_name = (msg['from']['first_name'], msg['from']['last_name'])
        #print(chat_id, user_name, *real_name)

        message = msg['text']  #.lower()
        
        print(msg['from'])    
        print(message)
        dbr.add_user(msg["from"])
        
        if message.startswith("/"): #COMMAND
            if message == "/info":
                loop.create_task(self.sender.sendMessage("Di quale mensa vuoi informazioni?"))
                self.Flow[chat_id] = "info" #Imposta stato dell'utente su INFO
        
        elif chat_id in self.Flow:  #FLOW
            if self.Flow[chat_id] == "info":
                loop.create_task(self.SendInfo(msg))
            del self.Flow[chat_id]
        else:
            loop.create_task(self.SendMenu(msg))

    async def SendMenu(self, msg):
        message = msg['text'] #.lower()
        #if message.lower() in ["cammeo", "betti", "martiri", "rosellini"]:
        if dbr.get_id(message) is not None:
            await self.sender.sendMessage("Preparazione del menù in corso...")
            #loop.create_task(self.replyer(message))
            await getmen.makeimg(message)
            for x in dbr.get_image(message):
                stream = io.BytesIO()
                x.save(stream, "PNG")
                stream.seek(0)
                loop.create_task(self.sender.sendPhoto(('z.png', stream), caption=dbr.RndMsg(message), parse_mode="HTML"))
                print("Menu sent")
        else:
            loop.create_task(self.sender.sendMessage("no menù found"))

    async def SendInfo(self, msg):
        #COORDINATE
        lat, lon = dbr.get_coordinates(msg['text'])
        if lat is not None or lon is not None:
            await self.sender.sendLocation(latitude=lat, longitude=lon)
        else:
            await self.sender.sendMessage("Questa mensa non ha ancora le coordinate...")  

        #ORARI
        TimeTables = dbr.TimeTables(msg['text'], kind="PV")
        if len(TimeTables) > 0:
            loop.create_task(self.sender.sendMessage("\n".join([ttb.makeperiod(*Table) for Table in TimeTables])))
        else:
            loop.create_task(self.sender.sendMessage("Questa mensa non ha ancora gli orari..."))       

#Please, create a file named "token.txt" containing yout telegram token
#I made a separate unsynced file for privacy. so do it too
TOKEN = ""
with open(os.path.join(os.getcwd(), "token.txt"), 'r') as myfile:
    TOKEN=myfile.read().replace('\n', '') # get token from file

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Answerer, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()
