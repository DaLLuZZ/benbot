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

            current_datetime = datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800)
            string_datetime = current_datetime.strftime('%Y-%m-%d')
            print(current_datetime.strftime('%Y-%m-%d %H:%M'))
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

            schedule_header = response['schedule_header']
            schedule = response['schedule']

            message = ''

            weekday = current_datetime.isoweekday()
            # parsing this fucken json =/
            for bn in [1, 2, 3, 4, 5]:
                str = 'bell_{}'.format(bn)
                bell = schedule[str]
                str = 'day_{}'.format(weekday)
                day = bell[str]
                for lesson in day['lessons']:
                    message = message + '{}-я пара ({} - {})\n{} ({})\n'.format(bn, bell['header']['start_lesson'], bell['header']['end_lesson'], lesson['subject_name'], lesson['type'])
                    for teacher in lesson['teachers']:
                        message = message + teacher['name'] + ' (' + teacher['post'] + ')\n'
                    message = message + lesson['room_name'] + '\n\n'

            vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=message#response['schedule']['bell_1']['day_5']['lessons'][0]['teachers'][0]['name']
                )

if __name__ == '__main__':
    main()
