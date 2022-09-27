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

if __name__ == '__main__':
    main()
