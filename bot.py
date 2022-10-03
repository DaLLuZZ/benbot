import os
import requests

def GetNextChr(char):
    if char == 57:
        char = 65
    elif char == 90:
        char = 48
    else:
        char = char + 1
    return char

def bufGetNext(buffer):
    i = 5
    while i >= 0:
        buffer[i] = GetNextChr(buffer[i])
        if buffer[i] != 48:
            break;
        i = i - 1
    return buffer

def main():
    client = requests.Session()
    buffer = [48, 48, 48, 48, 48, 48]

    i = 0
    while i < 500:
        buffer = bufGetNext(buffer)
        print("https://lms.misis.ru/enroll/{}{}{}{}{}{}".format(chr(buffer[0]), chr(buffer[1]), chr(buffer[2]), chr(buffer[3]), chr(buffer[4]), chr(buffer[5])))
        i = i + 1
    
#    client = requests.get("https://lms.misis.ru/enroll/{}".format())


#    print(client.text)
#    course = ""
#    startpos = client.text.find("<title>Зарегистрироваться на ")
#    if startpos != -1:
#        print(startpos)
#        course = client.text[startpos+29:client.text.find("</title>")]
#        print(course)

if __name__ == '__main__':
    main()
