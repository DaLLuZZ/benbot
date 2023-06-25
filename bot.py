import requests
import json
import datetime
from datetime import datetime, date, time
import calendar

from mysql.connector import connect

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

def say_hello(vk, user_id):
    # отправить данному userid приветственное сообщение с клавиатурой
    keyboard = VkKeyboard()
    keyboard.add_button('Сегодня', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Завтра', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Выбрать группу', color=VkKeyboardColor.PRIMARY)
    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Какие запросы распознаёт бот?\n\n"сегодня" / "завтра" / "послезавтра"\n"[день недели]" (пример: "вторник" или "вт")\n\nТакже можно воспользоваться клавиатурой\n\nПеред началом работы необходимо выбрать интересующую Вас академическую группу ("Выбрать группу")'
    )

def main():
    client = requests.Session()

    # аргументом передаётся токен бота, убран из кода перед публикацией
    vk_session = vk_api.VkApi(token='')

    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    # подключаемся к серверу СУБД
    connection = connect(
        host="localhost",
        user="root",
        password="",
        buffered=True
    )
    cursor = connection.cursor(buffered=True)

    # импортируем базу данных с группами, если её нет на сервере (файл vkbot.sql должен находится в одном каталоге с bot.py)
    with open('vkbot.sql', 'r', encoding="utf-8") as sqlfile:
        commands = sqlfile.read().split(';')
        for command in commands:
            if command.strip() != '':
                cursor.execute(command)
                connection.commit()

    # dict, слушать ли сообщение с названием группы от пользователя с заданным userid (True/False)
    group_listening = {}

    # бот готов к работе
    print("MISIS BOT | I'm ready to start!")

    # главный цикл бота
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            # поскольку учебный семестр закончился, расписания на текущую и следующую неделю нет
            # принято решение в целях тестирования вычесть из текущей даты 60 календарных дней
            # с началом нового семестра достаточно убрать вычитаемое 2*30*24*60*60 для корректной работы бота
            current_timestamp = int(calendar.timegm(datetime.utcnow().utctimetuple())) + 10800 - 2*30*24*60*60 # msc = gmt + 3 hours - 2 months 
            current_datetime = datetime.utcfromtimestamp(current_timestamp)
            wishtime = current_datetime
            wishday = 'сегодня'

            # поиск написавшего боту пользователя в базе данных
            cursor.execute("SELECT `users`.`groupid`, `groups`.`acronym` FROM `users` INNER JOIN `groups` ON `users`.`groupid` = `groups`.`id` WHERE `users`.`userid` = {}".format(event.user_id))
            group_id = 0
            group_name = ''
            if cursor.rowcount != 0:
                for row in cursor:
                    group_id = row[0]
                    group_name = row[1]

            if event.text.lower() == 'выбрать группу':
                # если пользователь нажал кнопку "выбрать группу"
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Введите точное название группы с соблюдением регистра, например: БЭН-21-1"
                    )
                    # слушаем
                    group_listening.update({event.user_id: True})
                    continue
            elif group_listening.get(event.user_id):
                # если бот слушает сообщение с названием группы от данного userid
                new_group = event.text
                # поиск указанной группе в базе данных
                cursor.execute("SELECT `id` FROM `groups` WHERE `acronym` = \"{}\"".format(new_group))
                message = ''
                if cursor.rowcount == 0:
                    message = "Указанная группа \"{}\" не найдена в базе данных. Проверьте правильность написания".format(new_group)
                else:
                    for row in cursor:
                        # ставим группу пользователю
                        cursor.execute("DELETE FROM `users` WHERE `userid` = {}".format(event.user_id))
                        cursor.execute("INSERT INTO `users` (`userid`, `groupid`) VALUES ({}, {})".format(event.user_id, row[0]))
                        connection.commit()
                        message = "Указанная группа \"{}\" успешно установлена. Теперь вы можете в полной мере пользоваться ботом".format(new_group)
                        # прекращаем слушать
                        group_listening.update({event.user_id: False})
                vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=message)
                continue
            elif group_name == '':
                # если пользователь не указал группу - приветственное сообщение
                say_hello(vk, event.user_id)
                continue
            # обработка комманд пользователя - вычисление даты и дня недели
            elif event.text.lower() == 'сегодня' or event.text.lower() == 'today' or event.text.lower() == 'td' or event.text.lower() == 'сег':
                wishtime = current_datetime
                wishday = 'сегодня'
            elif event.text.lower() == 'завтра' or event.text.lower() == 'зав':
                wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + 86400) # msc + 1day = gmt + 3*60*60 + 24*60*60
                wishday = 'завтра'
            elif event.text.lower() == 'послезавтра' or event.text.lower() == 'пз':
                wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + 172800) # msc + 2days = gmt + 3*60*60 + 2*24*60*60
                wishday = 'послезавтра'
            elif event.text.lower() == 'понедельник' or event.text.lower() == 'пн':
                if current_datetime.isoweekday() > 1:
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (8 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующий понедельник'
            elif event.text.lower() == 'вторник' or event.text.lower() == 'вт':
                if current_datetime.isoweekday() > 2:
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (9 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующий вторник'
                elif current_datetime.isoweekday() < 2:
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (2 - current_datetime.isoweekday()) * 86400)
                    wishday = 'этот вторник'
            elif event.text.lower() == 'среда' or event.text.lower() == 'ср':
                if current_datetime.isoweekday() > 3:
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (10 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующую среду'
                elif current_datetime.isoweekday() < 3:
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (3 - current_datetime.isoweekday()) * 86400)
                    wishday = 'эту среду'
            elif event.text.lower() == 'четверг' or event.text.lower() == 'чт':
                if current_datetime.isoweekday() > 4:
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (11 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующий четверг'
                elif current_datetime.isoweekday() < 4:
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (4 - current_datetime.isoweekday()) * 86400)
                    wishday = 'этот четверг'
            elif event.text.lower() == 'пятница' or event.text.lower() == 'пт':
                if current_datetime.isoweekday() > 5:
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (12 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующую пятницу'
                elif current_datetime.isoweekday() < 5:
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (5 - current_datetime.isoweekday()) * 86400)
                    wishday = 'эту пятницу'
            elif event.text.lower() == 'суббота' or event.text.lower() == 'сб':
                if current_datetime.isoweekday() > 6:
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (13 - current_datetime.isoweekday()) * 86400)
                    wishday = 'следующую субботу'
                elif current_datetime.isoweekday() < 6:
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (6 - current_datetime.isoweekday()) * 86400)
                    wishday = 'эту субботу'
            elif event.text.lower() == 'воскресенье' or event.text.lower() == 'вс':
                    wishtime = datetime.utcfromtimestamp(current_timestamp + 10800 + (7 - current_datetime.isoweekday()) * 86400)
            else:
                # команда не распознана - приветственное сообщение
                say_hello(vk, event.user_id)
                continue

            # в воскресенье университет закрыт, занятий нет
            weekday = wishtime.isoweekday()
            if weekday == 7:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Воскресенье... Замечательный день...'
                )
                continue

            # готовим пейлоад для запроса к сайту МИСИС
            body =    {
                       'filial': 880,
                       'group': group_id,
                       'room': None,
                       'teacher': None,
                       'start_date': wishtime.strftime('%Y-%m-%d'),
                       'end_date': None
                       }
            client = requests.post('https://lk.misis.ru/method/schedule.get', body)
            response = json.loads(client.text)

            # расписания на выбранную неделю нет
            if response['status'].upper() != 'FOUND':
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Расписание не найдено =/'
                )
                continue

            schedule_header = response['schedule_header']
            schedule = response['schedule']

            # готовим сообщение для отправки пользователю
            message = ''

            # парсим json, полученный в ответ на запрос к сайту МИСИС, и здесь же начинаем заполнять строку с сообщением
            for bn in [1, 2, 3, 4, 5, 6, 7]:
                if not 'bell_{}'.format(bn) in schedule:
                    continue
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

            # если итоговое сообщение оказалось пустым (нет занятий в расписании в указанный день)
            if not message:
                message = 'Расписание не найдено =/'

            # отправляем сообщение пользователю
            message = 'Расписание для группы {} на {} {} ({})\n\n'.format(group_name, wishday, schedule_header['day_{}'.format(weekday)]['date'], schedule_header['day_{}'.format(weekday)]['short_text']) + message
            vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=message
                )

if __name__ == '__main__':
    main()
