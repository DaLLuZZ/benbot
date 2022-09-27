import os
import requests
import json
import datetime
from datetime import datetime, date, time
import calendar

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

def main():
    session = requests.Session()
    client = requests.Session()

    vk_session = vk_api.VkApi(token='3a1966' + 'a9dd09543a8b81ece18' + 'b57359fd6f5ef' + '449e7e64b6ecd' + 'df820b5f5d543c9f00' + 'f9e73c86'+ '40b5f3bf')

    vk = vk_session.get_api()

    # Get csrf token =/
    #client = requests.get('https://edu.misis.ru/schedule/moscow/current')
    #csrftoken = client.text[361:449] # should not be hardcoded probably yes???

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print('id{}: "{}"'.format(event.user_id, event.text), end=' ')

            current_datetime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800) # msc = gmt + 3*60*60
            wishtime = current_datetime
            wishday = 'сегодня'

            if event.text.lower() == 'сегодня' or event.text.lower() == 'ctujlyz' or event.text.lower() == 'today' or event.text.lower() == 'td' or event.text.lower() == 'сег' or event.text.lower() == 'сг' or event.text.lower() == 'cu' or event.text.lower() == 'с':
                wishtime = current_datetime
                wishday = 'сегодня'
            elif event.text.lower() == 'завтра' or event.text.lower() == 'pfdnhf' or event.text.lower() == 'з' or event.text.lower() == 'зав' or event.text.lower() == 'зв':
                wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + 86400) # msc + 1day = gmt + 3*60*60 + 24*60*60
                wishday = 'завтра'
            elif event.text.lower() == 'послезавтра' or event.text.lower() == 'gjcktpfdnhf' or event.text.lower() == 'пз':
                wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + 172800) # msc + 2days = gmt + 3*60*60 + 2*24*60*60
                wishday = 'послезавтра'
            elif event.text.lower() == 'понедельник' or event.text.lower() == 'пн':
                if current_datetime.isoweekday() > 1:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (8 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующий понедельник'
            elif event.text.lower() == 'вторник' or event.text.lower() == 'вт':
                if current_datetime.isoweekday() > 2:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (9 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующий вторник'
                elif current_datetime.isoweekday() < 2:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (2 - current_datetime.isoweekday()) * 86400)
                    wishday = 'этот вторник'
            elif event.text.lower() == 'среда' or event.text.lower() == 'ср':
                if current_datetime.isoweekday() > 3:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (10 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующую среду'
                elif current_datetime.isoweekday() < 3:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (3 - current_datetime.isoweekday()) * 86400)
                    wishday = 'эту среду'
            elif event.text.lower() == 'четверг' or event.text.lower() == 'чт':
                if current_datetime.isoweekday() > 4:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (11 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующий четверг'
                elif current_datetime.isoweekday() < 4:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (4 - current_datetime.isoweekday()) * 86400)
                    wishday = 'этот четверг'
            elif event.text.lower() == 'пятница' or event.text.lower() == 'пт':
                if current_datetime.isoweekday() > 5:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (12 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующую пятницу'
                elif current_datetime.isoweekday() < 5:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (5 - current_datetime.isoweekday()) * 86400)
                    wishday = 'эту пятницу'
            elif event.text.lower() == 'суббота' or event.text.lower() == 'сб':
                if current_datetime.isoweekday() > 6:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (13 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующую субботу'
                elif current_datetime.isoweekday() < 6:
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (6 - current_datetime.isoweekday()) * 86400)
                    wishday = 'эту субботу'
            elif event.text.lower() == 'воскресенье' or event.text.lower() == 'вс':
                    wishtime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 + (7 - current_datetime.isoweekday()) * 86400)
            elif event.text.lower() == 'дз' or event.text.lower() == 'lp' or event.text.lower() == 'домашка' or event.text.lower() == 'ljvfirf' or event.text.lower() == 'домашки':
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Ссылка на гугл док с домашками (credits to Maria):\nhttps://docs.google.com/spreadsheets/d/1008v3roUvGxZcNO6atvlsAhVPTd0loIOTUKmK8Xn-4o/edit'
                )
                continue
            else:
                keyboard = VkKeyboard()

                keyboard.add_button('Сегодня', color=VkKeyboardColor.POSITIVE)
                keyboard.add_line()
                keyboard.add_button('Завтра', color=VkKeyboardColor.POSITIVE)
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message='Какие запросы распознаёт бот?\n\n"сегодня" / "завтра" / "послезавтра"\n"[день недели]" (пример: "вторник" или "вт")\n"дз"\n\nТакже можно воспользоваться клавиатурой (функционал клавиатуры временно(?) ограничен)'
                )
                continue

            weekday = wishtime.isoweekday()
            if weekday == 7:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Воскресенье... Замечательный день...'
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

            client = requests.post('https://lk.misis.ru/method/schedule.get', body, headers)
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
                if not 'bell_{}'.format(bn) in schedule:
                    continue;
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
                    message=message
                )

if __name__ == '__main__':
    main()
