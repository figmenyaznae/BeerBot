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
    bot.send_message(message.chat.id,
        'Привет. Я всё ещё на стадии альфа-тестирования.'+
        'Пожалуйста, не разговаривай со мной если ты не мой создатель.\n\n'+
        'Hello, I\'m still in alpha-test mode,'+
        'please, don\'t speak to me if you are not my developer.')

def start_poll(chat, message):
    session = Session()
    if chat:
        chat.meeting = new_meeting
        chat.is_polling = True
    else:
        new_chat = Status(
            chat_id=message.chat.id,
            is_polling=True,
            meeting=new_meeting
        )
        session.add(new_chat)
    session.commit()

    announce = bot.send_message(
        message.chat.id,
        'Следующий бар ' + date_to_locale(new_meeting.date) + '\n'+
        'Пишите 🍻 если идете и 🥃 если нет.'
    )

    try:
        bot.pin_chat_message(message.chat.id, announce.message_id)
    except:
        pass

def create_meeting_option(message):
    session = Session()
    new_option = MeetingOption(
            chat_id = message.chat.id,
            user_id = message.from_user.id,
            message_id = message.message_id
        )

    meeting_date = None
    place_name = ''
    is_place = False
    for word in message.text.split(' '):
        try:
            meeting_date = parser.parse(word)
            is_place = False
        except:
            pass

        if is_place:
            place_name += ' ' + word

        if word in ['в']:
            is_place = True


    if place_name != '':
        new_option.name = place_name.strip()

    if meeting_date:
        new_option.date = meeting_date
        if place_name == '':
            bot.send_message(message.chat.id,
                '[{}](tg://user?id={}), куда пойдём?'.format(
                    get_user_name(message),
                    message.from_user.id
                ),
                parse_mode = 'Markdown'
            )
    else:
        bot.send_message(message.chat.id,
            '[{}](tg://user?id={}), когда назначить бар?'.format(
                get_user_name(message),
                message.from_user.id
            ),
            parse_mode = 'Markdown'
        )

    '''
    bot.send_message(message.chat.id,
        'Распознано: [{}](tg://user?id={}), предлагает сходить {} в {}'.format(
            get_user_name(message),
            message.from_user.id,
            new_option.date if new_option.date else 'дата не распознана',
            new_option.name if new_option.name else 'место не распознано'
        ),
        parse_mode = 'Markdown'
    )
    '''
    session.add(new_option)
    session.commit()

def parse_meeting_option(message):
    session = Session()
    for option in session.query(MeetingOption).filter_by(
        chat_id=message.chat.id,
        user_id=message.from_user.id
      ).all():
        if option.date is None:
            try:
                option.date = parser.parse(message.text[11:].strip())
                session.commit()
            except:
                bot.send_message(message.chat.id,
                    '[{}](tg://user?id={}), не могу распознать дату, повторите',format(
                        get_user_name(message),
                        message.from_user.id,
                        reply_to_message_id=option.message_id
                    ))
            finally:
                break
        if option.name is None:
            option.name = message.text[11:].strip()
            session.commit()
            break
    else:
        create_meeting_option(message)

def send_attendants(attendants):
    text = '\n'.join([
            u'{}: {}'.format(
                attendant.name,
                int_to_status(attendant.status)
            ) for attendant in chat.meeting.attendants
        ])
    if text=='':
        text = 'Никто пока не подтвердил своё участие'
    bot.send_message(message.chat.id, text)

def send_options(chat_id):
    session = Session()
    text = '\n'.join([
            u'Есть вариант пойти {} в {}'.format(
                option.date,
                option.name
            ) for option in session.query(MeetingOption).filter(
                MeetingOption.chat_id == chat_id,
                MeetingOption.date != None,
                MeetingOption.name != None
            ).all()
        ])
    bot.send_message(chat_id, text)

def is_polling(message):
    session = Session()
    chat = session.query(Status).get(message.chat.id);

    if chat:
        return chat.is_polling
    else:
        return False

@bot.message_handler(regexp='(?m)^@fb1488_bot')
def bot_mentioned(message):
    session = Session()
    chat = session.query(Status).get(message.chat.id)

    if chat and chat.is_polling:
        if (message.text[11:].strip() in [
            'че как?',
            'кто пойдет?',
            'кто идет?',
            'состав'
          ]):
            send_attendants(chat.meeting.attendants)
        else:
            start_poll(chat, message)
    else:
        if (message.text[11:].strip() in [
            'варианты'
          ]):
            send_options(message.chat.id)
        elif session.query(MeetingOption).filter_by(
            chat_id=message.chat.id,
            user_id=message.from_user.id
          ).count()==0:
            create_meeting_option(message)
        else:
            parse_meeting_option(message)

@bot.message_handler(func=is_polling)
def echo_all(message):
    status = text_to_status(message.text)
    if not status is None:
        session = Session()
        chat = session.query(Status).get(message.chat.id)

        if chat and chat.meeting:
            attendance = session.query(MeetingAttendant).get((
                message.from_user.id,
                chat.meeting_id
            ))

            if not attendance:
                session.add(MeetingAttendant(
                    id = message.from_user.id,
                    name = get_user_name(message),
                    status = status_to_int(status),
                    meeting=chat.meeting
                ))
            else:
                attendance.status = status_to_int(status)

            session.commit()

bot.polling()