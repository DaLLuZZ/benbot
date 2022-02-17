# -*- coding: utf-8 -*-

import requests

<meta name="csrf-token" content="6k4ott1DgIAkfazE3zvn5XTHlEupgAyK3ru8/2UgD6thkfU/yBiOoJ5OkP80jwDpFPhwgqkWJmwsV9/KH5aJoA==" />


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
    
    client = requests.get('https://edu.misis.ru/schedule/moscow/current')
    if 'csrftoken' in client.cookies:
    # Django 1.6 and up
        csrftoken = client.cookies['csrftoken']
    else:
    # older versions
        csrftoken = client.cookies['csrf']

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print('id{}: "{}"'.format(event.user_id, event.text), end=' ')

            response = session.get(
                'http://api.duckduckgo.com/',
                params={
                    'q': event.text,
                    'format': 'json'
                }
            ).json()

            text = response.get('AbstractText')
            image_url = response.get('Image')

            if not text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=csrftoken
                )
                print('no results')
                continue

            attachments = []

            if image_url:
                image = session.get(image_url, stream=True)
                photo = upload.photo_messages(photos=image.raw)[0]

                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )

            vk.messages.send(
                user_id=event.user_id,
                attachment=','.join(attachments),
                random_id=get_random_id(),
                message=text
            )
            print('ok')


if __name__ == '__main__':
    main()
