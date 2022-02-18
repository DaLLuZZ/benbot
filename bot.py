# -*- coding: utf-8 -*-

import requests
import json

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
    client = requests.get('https://edu.misis.ru/schedule/moscow/current')
    csrftoken = client.text[361:449] # should not be hardcoded probably yes???

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print('id{}: "{}"'.format(event.user_id, event.text), end=' ')

            headers = {
                       'content-type': 'application/json;charset=UTF-8',
                       'authority': 'login.misis.ru',
                       'path': '/method/schedule.get',
                       'accept': 'application/json',
                       'x-csrf-token': csrftoken,
                       'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                       'sec-ch-ua-mobile': '?0',
                       'sec-ch-ua-platform':'"Windows"',
                       'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
                       'origin': 'https://edu.misis.ru',
                       'sec-fetch-site': 'same-site',
                       'sec-fetch-mode': 'cors',
                       'sec-fetch-dest': 'empty',
                       'referer': 'https://edu.misis.ru/',
                       'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
                      }
            body =    {
                       'filial': 880,
                       'group': '7121',
                       'room': None,
                       'teacher': None,
                       'start_date': '2022-02-18',
                       'end_date': None
                       }

            client = requests.post('https://login.misis.ru/method/schedule.get', body, headers)
            response = json.loads(client.text)

            vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=response['schedule']['bell_1']['day_5']['lessons'][0]['teachers'][0]['name']
                )


if __name__ == '__main__':
    main()
