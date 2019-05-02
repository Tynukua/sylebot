import json
from requests import get,post

class SimpleBot:#Об'єкт бота
    #Передача токену та перший апдейт
    def __init__(self, a):
        self.core = 'https://api.telegram.org/bot' + a
        self.firstUpdate = []
        
        while len(self.firstUpdate)==0:
            self.firstUpdate = self.getUpdates(offset = -1)
        self.firstUpdate = self.firstUpdate[0]['update_id']+1
    
    #Методи з Bot API
    def getMe(self):
        return get(f'{self.core}/getMe').json()
    
    #offset #limit #timeout #allowed_updates
    def getUpdates(self, **kwargs):
        
        #offset 
        #limit 
        #timeout 
        #allowed_updates
        
        self.Updates = None
        while self.Updates==None: 
            self.Updates = get(f'{self.core}/getUpdates', params = kwargs).json().get('result')
        return self.Updates
    def sendMessage(self, **kwargs ):
        #chat_id
        #text
        #parse_mode
        #disable_web_page_preview
        #disable_notification
        #reply_to_message_id}
        
        return get(f'{self.core}/sendMessage', params = kwargs).json()

    def forwardMessage(self, **kwargs):
        #chat_id, 
        #from_chat_id,
        #message_id, 
        #disable_notification 
        
        return get(f'{self.core}/forwardMessage', params = kwargs).json()

    def send_file(self, filename='text.txt', chat_id=''):
        file = open(filename, 'rb')
        send = f'{self.core}/sendDocument?chat_id=' + str(chat_id) 
        file.close()
        return post(send, files={'document': file})
#Витягування даних з словника за шляхом у листі
def get_hang(update, tuplekeys):
    if type(tuplekeys) is tuple: pass
    elif type(tuplekeys) is list: tuplekeys = tuple(tuplekeys)
    else: return 
    
    for i in tuplekeys:
        if type(update) is dict: 
            update = update.get(i)
        elif type(update) is list and type(i) is int: 
            if i <= len(update): 
                update = update[i]
        elif not update: 
            return 
        else: 
            return 
        
    return update

class NotSimple:
    def __init__(self, Update):
        self.Update = Update
    #додавання id користувачів до JSON файлу
    def add_id(self):
        data = []
        way = ('message','chat','id')
        ids = get_hang(self.Update, way )
        if not ids: return 

        with open('user.json','rt') as database:
            data = json.load(database)
        users= data['users']+data['chats']

        if ids in users: return
        else:
            if ids>0:
                data['users'].append(ids)
            if ids<0:
                data['chats'].append(ids)
        
        with open('user.json','wt') as database:
            json.dump(data, database)
        
        return True

    #Обробник тексту
    def text_handler(self, a = 'Hello'):
        a = a.lower()
        way1,way2 = ('message','text'),('edited_message','text')
        mess,edmess = get_hang(self.Update, way1).lower, get_hang(self.Update, way2)
        
        if not mess:
            mess = mess.lower()
            if mess.find(a)>-1: return True, way1

        elif not edmess: 
            edmess = edmess.lower()
            if edmess.find(a)>-1: return True, way2

        else: return False, 
        return False, 

    #Обробник команд
    def cmd_handler(self, a = 'start', split = ' '):
        a = a.lower()
        entity = get_hang(self.Update, ('message','entities',0))
        if entity.get('type') !=  'bot_command': return False, 
        
        lenc = entity.get('length')
        lena = len(a)
        textcmd = get_hang(self.Update,('message','text')).lower()[1:]
        cmd = textcmd[:lena] 
        if cmd == a: return True, textcmd[lena:].split(split)
        else: return False, 
        return False, 

    #Відображення апдейту на екрані
def jprint( message,n = 1):
    tmp = ''
    i = -1
    for x in str(message):
            
        if x =='{': 
            i+=1
            tmp+='\n'+i*'\t'*n
        elif x == ',': tmp+='\n'+i*'\t'*n
        elif x == '}': 
            i-=1
            tmp+=i*'\t'*n
        else: tmp+=x
    print( tmp)

