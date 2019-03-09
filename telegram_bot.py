import asyncio
import os
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
import menu_retrieve as getmen

class Answerer(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Answerer, self).__init__(*args, **kwargs)

    async def on_chat_message(self, msg):
        chat_id = msg['chat']['id']
        message = msg['text']  #.lower()
        uname = msg['chat']['username']

        if message.lower() in ["cammeo", "betti", "martiri", "rosellini"]:
            img_path = await getmen.makeimg(message)

            await self.sender.sendPhoto(open(img_path, 'rb'))
        else:
            await self.sender.sendMessage("no menù found")

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
