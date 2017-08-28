import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from settings import *
from dateutil import parser
from datetime import datetime


bot = telebot.TeleBot(BOT_TOKEN)
engine = create_engine('sqlite:///test.db')#, echo=True)

Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hello, I\'m still in alpha-test mode, please, don\'t speak to me if you are not my developer.')

@bot.message_handler(regexp='(?m)^@fb1488_bot')
def start_poll(message):
    session = Session()    
    chat = session.query(Status).get(message.chat.id)
    if chat and (message.text[11:].strip()=='status'):
        bot.send_message(message.chat.id, '\n'.join([
                u'{}: {}'.format(attendant.name, attendant.status)
                for attendant in chat.meeting.attendants
            ]))
    else:
        meeting_date = None
        for word in message.text.split(' '):
            try:
                meeting_date = parser.parse(word)
                break
            except:
                pass
        if meeting_date:
            new_meeting = Meeting(date=meeting_date)
            session.add(new_meeting)
            if chat:
                chat.meeting = new_meeting
                chat.is_polling = True
            else:
                new_chat = Status(chat_id=message.chat.id, is_polling=True, meeting=new_meeting)
                session.add(new_chat)
            session.commit()
            announce = bot.send_message(message.chat.id, 'Next meeting on ' + new_meeting.date.strftime('%d. %B %Y(%A)'))
            try:
                bot.pin_chat_message(message.chat.id, announce.message_id)
            except:
                pass    
        else:
            bot.send_message(message.chat.id, 'What day should next meeting be?')    

def get_user_name(message):
    return '{} {}'.format(message.from_user.first_name, message.from_user.last_name)

def is_polling(message):
    session = Session()
    chat = session.query(Status).get(message.chat.id);
    if chat:
        return chat.is_polling
    else:
        return False

@bot.message_handler(func=is_polling)
def echo_all(message):
    session = Session()
    bot.send_message(message.chat.id,  get_user_name(message) + ' just said: ' + message.text)
    chat = session.query(Status).get(message.chat.id)
    if chat:
        session.add(MeetingAttendant(name=get_user_name(message), status=u'\U0001F37B', meeting=chat.meeting))
        session.commit()

bot.polling()