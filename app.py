from flask import Flask, request
import requests, json

BOT_TOKEN = '398858338:AAGMhLrE_eNfLwKOfeFQuLhlEH7g878_fOg'
URL = 'https://api.telegram.org/bot%s/' % BOT_TOKEN
MyURL = 'https://fb1488bot.herokuapp.com/'

api = requests.Session()
set_hook = api.get(URL + 'setWebhook?url=%s' % MyURL)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method=='POST':
        try:
            message = json.loads(request.data)['message']
            api.post(URL + 'sendMessage', data={
                    'chat_id': message['chat']['id'],
                    'text': 'You sent me' + message['text']
                })
            return 'OK'
        except:
            raise Exception(request.data)    
    else:
        return 'Hello, I\'m still in alpha-test mode, please, don\'t speak to me if you are not my developer.'
