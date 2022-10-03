import os
import requests

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
    buffer = [48, 48, 48, 48, 48, 47]

    i = 0
    while i < 500:
        i = i + 1

        buffer = bufGetNext(buffer)
        url = "https://lms.misis.ru/enroll/{}{}{}{}{}{}".format(chr(buffer[0]), chr(buffer[1]), chr(buffer[2]), chr(buffer[3]), chr(buffer[4]), chr(buffer[5]));
        client = requests.get(url)

        print("[{}] {}".format(client.status_code, url))
        course = ""
        if client.status_code != 404: # course exists
            course = client.text[client.text.find("<title>Зарегистрироваться на ") + 29:client.text.find("</title>")]
            print("FOUND: \n" + course)

if __name__ == '__main__':
    main()
