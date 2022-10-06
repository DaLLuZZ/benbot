import os
import requests
from datetime import datetime
import calendar
from prettytable import PrettyTable

def bufGetNext(buffer):
    i = 5
    while i >= 0:
        if buffer[i] == 57:
            buffer[i] = 65
        elif buffer[i] == 90:
            buffer[i] = 48
        else:
            buffer[i] = buffer[i] + 1

        if buffer[i] != 48:
            break;
        i = i - 1

    return buffer

def main():
    client = requests.Session()
    buffer = [48, 48, 48, 48, 48, 48]

    table = PrettyTable()
    table.field_names = ["№ п/п", "Наименование курса", "Ссылка для регистрации"]

    log = open('log.txt', 'w')
    outfile = open('output.txt', 'w')
    outfiletable = open('table.txt', 'w')
    outfiletable.write("Доступные для регистрации курсы на {}\n".format(datetime.utcfromtimestamp(int(calendar.timegm(datetime.utcnow().utctimetuple()))).strftime('%H:%M:%S %d-%m-%Y')))

#    testing
#    https://lms.misis.ru/enroll/HLTTBM
#    buffer = [ord('Z'), ord('Z'), ord('Z'), ord('Z'), ord('Z'), ord('0')]

    found = 0
    i = 0
    while buffer[0] != 90 or buffer[1] != 90 or buffer[2] != 90 or buffer[3] != 90 or buffer[4] != 90 or buffer[5] != 90:
        url = "https://lms.misis.ru/enroll/{}{}{}{}{}{}".format(chr(buffer[0]), chr(buffer[1]), chr(buffer[2]), chr(buffer[3]), chr(buffer[4]), chr(buffer[5]))

        try:
            client = requests.get(url)
        except BaseException as err:
            print("{}: {}".format(type(err), err))
            log.write("{}: {}\n".format(type(err), err))
            continue

        print("[{}] [{}] [{}] {}".format(found, i, client.status_code, url))
        course = ""
        if client.status_code == 200:
            found = found + 1
            course = client.text[client.text.find("<title>Зарегистрироваться на ") + 29:client.text.find("</title>")]
            outfile.write(url + "\n" + course + "\n")
            table.add_row([found, course, url])
            print("FOUND: " + course)
        log.write("[{}] [{}] [{}] {}{}{}{}{}{}\n".format(found, i, client.status_code, chr(buffer[0]), chr(buffer[1]), chr(buffer[2]), chr(buffer[3]), chr(buffer[4]), chr(buffer[5])))
        buffer = bufGetNext(buffer)
        i = i + 1

    outfiletable.write(str(table))
    log.close()
    outfile.close()
    outfiletable.close()

if __name__ == '__main__':
    main()
