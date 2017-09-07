locale_week=['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
locale_month=['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

def date_to_locale(date):
    return '{} {} {} ({})'.format(date.day, locale_month[date.month-1], date.year, locale_week[date.weekday()])

def get_user_name(message):
    user = message.from_user
    if user.first_name:
        if user.last_name:
            return '{} {}'.format(user.first_name, user.last_name)
        else:
            return user.first_name
    else:
        return user.username

def status_to_int(status):
    return 1 if status else 0

def int_to_status(status):
    return '🍻' if status else '🥃'

def text_to_status(text):
    status = None
    if text == '🍻':
        status = True
    elif text == '🥃': 
        status = False

    return status