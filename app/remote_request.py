from time import sleep
import requests


url = "https://codegeneratemoney.onrender.com/"

if __name__ == '__main__':
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            print(response.text)
        else:
            print(response.status_code)
        sleep(10)
    pass
