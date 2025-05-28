from time import sleep
import requests
from  datetime import datetime

url = "https://codegeneratemoney.onrender.com/"

if __name__ == '__main__':
    while True:
        response = requests.get(url,data={'name':'strategy_one'})
        if response.status_code == 200:
            print(datetime.now(),response.text)
        else:
            print(response.status_code)
        sleep(2*60)
    pass
