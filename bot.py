import os
import requests
import json
import datetime
from datetime import datetime, date, time
import calendar

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

def main():
    session = requests.Session()
    client = requests.Session()
    
    # Авторизация пользователя:
    """
    login, password = 'python@vk.com', 'mypassword'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    """

    # Авторизация группы (для групп рекомендуется использовать VkBotLongPoll):
    # при передаче token вызывать vk_session.auth не нужно
    vk_session = vk_api.VkApi(token='3a1966a9dd09543a8b81ece18b57359fd6f5ef449e7e64b6ecddf820b5f5d543c9f00f9e73c8640b5f3bf')

    vk = vk_session.get_api()

    # Get csrf token =/
    #client = requests.get('https://edu.misis.ru/schedule/moscow/current')
    #csrftoken = client.text[361:449] # should not be hardcoded probably yes???

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print('id{}: "{}"'.format(event.user_id, event.text), end=' ')

            current_datetime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800) # msc = gmt + 3*60*60
            wishtime = current_datetime
            wishday = 'сегодня'
            if event.text.lower() == 'завтра' or event.text.lower() == 'pfdnhf':
                wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + 86400) # msc + 1day = gmt + 3*60*60 + 24*60*60
                wishday = 'завтра'
            elif event.text.lower() == 'послезавтра' or event.text.lower() == 'gjcktpfdnhf':
                wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + 172800) # msc + 2days = gmt + 3*60*60 + 2*24*60*60
                wishday = 'послезавтра'
            elif event.text.lower() == 'понедельник' or event.text.lower() == 'пн':
                if current_datetime.isoweekday() > 1:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (8 - current_datetime.isoweekday()) * 86400)
                    wishday = 'ближайший понедельник'
            elif event.text.lower() == 'вторник' or event.text.lower() == 'вт':
                if current_datetime.isoweekday() > 2:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (9 - current_datetime.isoweekday()) * 86400)
                    wishday = 'ближайший вторник'
                elif current_datetime.isoweekday() < 2:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (2 - current_datetime.isoweekday()) * 86400)
                    wishday = 'вторник'
            elif event.text.lower() == 'среда' or event.text.lower() == 'ср':
                if current_datetime.isoweekday() > 3:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (10 - current_datetime.isoweekday()) * 86400)
                    wishday = 'ближайшую среду'
                elif current_datetime.isoweekday() < 3:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (3 - current_datetime.isoweekday()) * 86400)
                    wishday = 'среду'
            elif event.text.lower() == 'четверг' or event.text.lower() == 'чт':
                if current_datetime.isoweekday() > 4:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (11 - current_datetime.isoweekday()) * 86400)
                    wishday = 'ближайший четверг'
                elif current_datetime.isoweekday() < 4:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (4 - current_datetime.isoweekday()) * 86400)
                    wishday = 'четверг'
            elif event.text.lower() == 'пятница' or event.text.lower() == 'пт':
                if current_datetime.isoweekday() > 5:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (12 - current_datetime.isoweekday()) * 86400)
                    wishday = 'ближайшую пятницу'
                elif current_datetime.isoweekday() < 5:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (5 - current_datetime.isoweekday()) * 86400)
                    wishday = 'пятницу'
            elif event.text.lower() == 'суббота' or event.text.lower() == 'сб':
                if current_datetime.isoweekday() > 6:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (13 - current_datetime.isoweekday()) * 86400)
                    wishday = 'ближайшую субботу'
                elif current_datetime.isoweekday() < 6:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (6 - current_datetime.isoweekday()) * 86400)
                    wishday = 'субботу'
            elif event.text.lower() == 'воскресенье' or event.text.lower() == 'вс':
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (7 - current_datetime.isoweekday()) * 86400)
            elif event.text.lower() == 'дз' or event.text.lower() == 'lp':
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Ссылка на таблицу с домашнкой (credits to Maria):\nhttps://docs.google.com/spreadsheets/d/1008v3roUvGxZcNO6atvlsAhVPTd0loIOTUKmK8Xn-4o/edit'
                )

            weekday = wishtime.isoweekday()
            if weekday == 7:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Воскресенье...'
                )
                continue

            string_datetime = wishtime.strftime('%Y-%m-%d')
            print(wishtime.strftime('%Y-%m-%d %H:%M'))

            headers = {
                       #'x-csrf-token': csrftoken, # no necessity to pass csrf token in header wtf why omfg o_0 ??
                      }
            body =    {
                       'filial': 880,
                       'group': '7121',
                       'room': None,
                       'teacher': None,
                       'start_date': string_datetime,
                       'end_date': None
                       }

            client = requests.post('https://login.misis.ru/method/schedule.get', body, headers)
            print(client.text)
            response = json.loads(client.text)

            if response['status'].upper() != 'FOUND':
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Расписание не найдено =/'
                )
                
            schedule_header = response['schedule_header']
            schedule = response['schedule']

            message = ''

            # parsing this fucken json =/
            for bn in [1, 2, 3, 4, 5]:
                bell = schedule['bell_{}'.format(bn)]
                day = bell['day_{}'.format(weekday)]
                for lesson in day['lessons']:
                    message = message + '{}-я пара ({} - {})\n{} ({})\n'.format(bn, bell['header']['start_lesson'], bell['header']['end_lesson'], lesson['subject_name'], lesson['type'])
                    for teacher in lesson['teachers']:
                        if not teacher['name'] or not teacher['post']:
                            continue
                        else:
                            message = message + teacher['name'] + ' (' + teacher['post'] + ')\n'
                    message = message + lesson['room_name'] + '\n\n'

            if not message:
                message = 'Расписание не найдено =/'

            message = 'Расписание для группы БЭН-21-2 на {} {} ({})\n\n'.format(wishday, schedule_header['day_{}'.format(weekday)]['date'], schedule_header['day_{}'.format(weekday)]['short_text']) + message
            vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=message#response['schedule']['bell_1']['day_5']['lessons'][0]['teachers'][0]['name']
                )

if __name__ == '__main__':
    main()
