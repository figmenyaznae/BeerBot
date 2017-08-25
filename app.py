from flask import Flask, request
import requests, json

BOT_TOKEN = "398858338:AAGMhLrE_eNfLwKOfeFQuLhlEH7g878_fOg"
URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
MyURL = "https://fb1488bot.herokuapp.com/"

api = requests.Session()
set_hook = api.get(URL + "setWebhook?url=%s" % MyURL)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    if 'text' in json.loads(request.data):
        return 'You sent me' + json.loads(request.data)['text']
    else:
        raise Exception(request.data)
    return "Hello, I'm still in alpha-test mode, please, don't speak to me if you are not my developer."
