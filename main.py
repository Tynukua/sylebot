from sylebot import SimpleBot, NotSimple, jprint
import json

bot = SimpleBot('666666:token')
offset = bot.firstUpdate
Updates = bot.getUpdates(offset = offset)

while True:
    while len(Updates)==0:
        Updates = bot.getUpdates(offset = offset+1)
    
    for i in Updates:
        Update = NotSimple(i)
        jprint(i)
        Update.add_id()
        
    offset = Updates[-1]['update_id']+1
    Updates = bot.getUpdates(offset = offset)
