import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from settings import *
from utils import *
from dateutil import parser
from datetime import datetime


bot = telebot.TeleBot(BOT_TOKEN)
engine = create_engine('sqlite:///test.db')

Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет. Я всё ещё на стадии альфа-тестирования.'+
        'Пожалуйста, не разговаривай со мной если ты не мой создатель.\n\n'+
        'Hello, I\'m still in alpha-test mode, please, don\'t speak to me if you are not my developer.')

def start_poll(session, chat, message):
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

        announce = bot.send_message(message.chat.id, 'Следующий бар ' + date_to_locale(new_meeting.date) + '\n'+
            'Пишите 🍻 если идете и 🥃 если нет.')

        try:
            bot.pin_chat_message(message.chat.id, announce.message_id)
        except:
            pass    
    else:
        bot.send_message(message.chat.id, 'Когда назначить бар?')    

@bot.message_handler(regexp='(?m)^@fb1488_bot')
def bot_mentioned(message):
    session = Session()    
    chat = session.query(Status).get(message.chat.id)
    if chat and (message.text[11:].strip() in ['че как?', 'кто пойдет?', 'кто идет?', 'состав']):
        text = '\n'.join([
                u'{}: {}'.format(attendant.name, '🍻' if attendant.status else '🥃')
                for attendant in chat.meeting.attendants
            ]);
        if text=='': text = 'Никто пока не подтвердил своё участие'
        bot.send_message(message.chat.id, text)
    else: start_poll(session, chat, message)


def is_polling(message):
    session = Session()
    chat = session.query(Status).get(message.chat.id);

    if chat:
        return chat.is_polling
    else:
        return False

@bot.message_handler(func=is_polling)
def echo_all(message):
    status = None
    if message.text == '🍻':
        status = True
    elif message.text == '🥃': 
        status = False
    if not status is None:
        session = Session()
        chat = session.query(Status).get(message.chat.id)

        if chat and chat.meeting:
            attendance = session.query(MeetingAttendant).get((message.from_user.id, chat.meeting_id))

            if not attendance:
                session.add(MeetingAttendant(id = message.from_user.id, name = get_user_name(message), status = status_to_int(status), meeting=chat.meeting))
            else:
                attendance.status = status_to_int(status)

            session.commit()

bot.polling()